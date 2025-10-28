import json
import csv
import io
from typing import List, Dict, Any

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate
from app.crud import user as crud_user
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate

def get_organizations(db: Session) -> List[Organization]:
    return db.query(Organization).all()

def get_organization(db: Session, org_id: int) -> Organization:
    return db.query(Organization).filter(Organization.id == org_id).first()

def get_all_descendant_orgs(db: Session, org_id: int) -> List[Organization]:
    descendants = []
    children = db.query(Organization).filter(Organization.parent_id == org_id).all()
    for child in children:
        descendants.append(child)
        descendants.extend(get_all_descendant_orgs(db, child.id))
    return descendants

def create_organization(db: Session, org: OrganizationCreate) -> Organization:
    db_org = Organization(
        name=org.name,
        level=org.level,
        parent_id=org.parent_id,
        department_grade=org.department_grade
    )
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org


def update_organization(db: Session, db_org: Organization, org_in: "OrganizationUpdate") -> Organization:
    update_data = org_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_org, field, value)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org


def delete_organization(db: Session, org_id: int) -> Organization:
    db_org = db.query(Organization).filter(Organization.id == org_id).first()
    if db_org:
        db.delete(db_org)
        db.commit()
    return db_org

def sync_organizations_from_file(db: Session, file: UploadFile) -> Dict[str, Any]:
    content = file.file.read()
    file_content = content.decode("utf-8")

    if file.filename.endswith(".json"):
        try:
            data = json.loads(file_content)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    elif file.filename.endswith(".csv"):
        raise NotImplementedError("CSV processing is not yet implemented.")
    else:
        raise ValueError("Unsupported file type")

    if not isinstance(data, list):
        raise ValueError("File content should be a list of organization objects")

    existing_orgs_by_name = {org.name: org for org in get_organizations(db)}
    incoming_orgs_by_name = {org_data["name"]: org_data for org_data in data if "name" in org_data}

    created_count = 0
    updated_count = 0

    # 1st Pass: Create/Update organizations
    for name, org_data in incoming_orgs_by_name.items():
        if name in existing_orgs_by_name:
            org_model = existing_orgs_by_name[name]
            org_model.level = org_data.get("level", org_model.level)
            db.add(org_model)
            updated_count += 1
        else:
            new_org = Organization(name=name, level=org_data.get("level"), parent_id=None)
            db.add(new_org)
            created_count += 1
    db.commit()

    # 2nd Pass: Set parent-child relationships
    all_orgs_by_name = {org.name: org for org in get_organizations(db)}
    for name, org_data in incoming_orgs_by_name.items():
        parent_name = org_data.get("parent_name")
        if parent_name and parent_name in all_orgs_by_name:
            org_model = all_orgs_by_name[name]
            parent_model = all_orgs_by_name[parent_name]
            org_model.parent_id = parent_model.id
            db.add(org_model)

    # 3rd Pass: Delete old organizations
    deleted_count = 0
    for name, org_model in existing_orgs_by_name.items():
        if name not in incoming_orgs_by_name:
            db.delete(org_model)
            deleted_count += 1

    db.commit()

    return {
        "status": "success",
        "created": created_count,
        "updated": updated_count,
        "deleted": deleted_count
    }

def sync_organizations_and_users_from_json(db: Session, file: UploadFile) -> Dict[str, Any]:
    content = file.file.read()
    try:
        chart_data = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format")

    stats = {"orgs_created": 0, "orgs_updated": 0, "users_created": 0, "users_updated": 0}

    def _get_leader_role(org_data: Dict) -> UserRole:
        # Level 3 (Team): No sub-organizations
        if not org_data.get("sub_organizations"):
            return UserRole.TEAM_LEAD
        
        # Level 2 (Department): All sub-organizations are teams
        is_dept_head = True
        for sub_org in org_data["sub_organizations"]:
            if sub_org.get("sub_organizations"):
                is_dept_head = False
                break
        if is_dept_head:
            return UserRole.DEPT_HEAD

        # Level 1 (Center/HQ): Anything above a department
        return UserRole.CENTER_HEAD

    def _process_user(user_data: Dict, org_id: int, role: UserRole):
        if not user_data:
            return

        email = user_data.get("email")
        if not email:
            email = "null@suresofttech.com"

        user = crud_user.user.get_by_email(db, email=email)
        
        full_name = user_data.get("name")
        title = user_data.get("title")

        if user:
            # Update existing user
            user_update_data = UserUpdate(
                full_name=full_name,
                title=title,
                organization_id=org_id,
                role=role
            )
            crud_user.user.update(db, db_obj=user, obj_in=user_update_data)
            stats["users_updated"] += 1
        else:
            # Create new user
            username = email.split('@')[0]
            password = username
            user_create_data = UserCreate(
                username=username,
                email=email,
                password=password,
                full_name=full_name,
                title=title,
                organization_id=org_id,
                role=role
            )
            crud_user.user.create(db, obj_in=user_create_data)
            stats["users_created"] += 1

    def _sync_recursive(org_data: Dict, parent_id: int = None):
        org_name = org_data["name"]
        
        # Find existing organization by name and parent
        existing_org = db.query(Organization).filter_by(name=org_name, parent_id=parent_id).first()

        if existing_org:
            db_org = existing_org
            stats["orgs_updated"] += 1
        else:
            # Simple level calculation based on depth, can be refined
            level = parent_id and db.query(Organization).get(parent_id).level + 1 or 1
            db_org = Organization(name=org_name, parent_id=parent_id, level=level)
            db.add(db_org)
            db.commit()
            db.refresh(db_org)
            stats["orgs_created"] += 1

        # Process leader
        leader_role = _get_leader_role(org_data)
        _process_user(org_data.get("leader"), db_org.id, leader_role)

        # Process members
        for member_data in org_data.get("members", []):
            _process_user(member_data, db_org.id, UserRole.EMPLOYEE)

        # Recurse for sub-organizations
        for sub_org_data in org_data.get("sub_organizations", []):
            _sync_recursive(sub_org_data, parent_id=db_org.id)

    for root_org_data in chart_data:
        _sync_recursive(root_org_data)

    return stats