
import json
import csv
import io
from typing import List, Dict, Any

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate

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
