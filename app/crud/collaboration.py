from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict
from collections import Counter

from app.crud.base import CRUDBase
from app.models.collaboration import CollaborationInteraction, InteractionType
from app.models.user import User
from app.models.project_member import ProjectMember
from app.models.organization import Organization
from app.schemas.collaboration import CollaborationInteractionCreate, CollaborationData, CollaborationGraph, CollaborationAnalysis, CollaborationNode, CollaborationEdge


class CRUDCollaborationInteraction(CRUDBase[CollaborationInteraction, CollaborationInteractionCreate, None]):
    
    def get_collaboration_data(
        self, 
        db: Session, 
        *, 
        project_id: Optional[int] = None, 
        organization_id: Optional[int] = None
    ) -> CollaborationData:
        query = db.query(CollaborationInteraction)
        
        if project_id:
            query = query.filter(CollaborationInteraction.project_id == project_id)
        
        if organization_id:
            # Get all users in the specified organization and its sub-organizations
            org_and_descendants = db.query(Organization).filter(Organization.id == organization_id).cte(name="org_and_descendants", recursive=True)
            org_and_descendants = org_and_descendants.union_all(
                db.query(Organization).filter(Organization.parent_id == org_and_descendants.c.id)
            )
            org_user_ids = db.query(User.id).join(org_and_descendants, User.organization_id == org_and_descendants.c.id).subquery()
            
            query = query.filter(
                (CollaborationInteraction.source_user_id.in_(org_user_ids)) |
                (CollaborationInteraction.target_user_id.in_(org_user_ids))
            )

        interactions = query.all()

        # Build Graph
        nodes_map: Dict[int, User] = {}
        edges_counter = Counter()
        
        for interaction in interactions:
            if interaction.source_user_id not in nodes_map:
                nodes_map[interaction.source_user_id] = interaction.source_user
            if interaction.target_user_id not in nodes_map:
                nodes_map[interaction.target_user_id] = interaction.target_user
            
            # Ensure edge is always (smaller_id, larger_id) to avoid duplicates
            edge = tuple(sorted((interaction.source_user_id, interaction.target_user_id)))
            edges_counter[edge] += 1

        nodes = [CollaborationNode(id=user.id, label=user.full_name, value=1) for user in nodes_map.values()]
        edges = [CollaborationEdge(source=u1, target=u2, value=count) for (u1, u2), count in edges_counter.items()]
        
        graph = CollaborationGraph(nodes=nodes, edges=edges)

        # Build Analysis
        review_counter = Counter(i.source_user_id for i in interactions if i.interaction_type == InteractionType.BITBUCKET_PR_REVIEW)
        help_counter = Counter(i.target_user_id for i in interactions if i.interaction_type == InteractionType.JIRA_MENTION)

        most_reviews = [{"user_id": uid, "count": count} for uid, count in review_counter.most_common(5)]
        most_help = [{"user_id": uid, "count": count} for uid, count in help_counter.most_common(5)]

        analysis = CollaborationAnalysis(most_reviews=most_reviews, most_help=most_help)

        return CollaborationData(graph=graph, analysis=analysis)


collaboration_interaction = CRUDCollaborationInteraction(CollaborationInteraction)
