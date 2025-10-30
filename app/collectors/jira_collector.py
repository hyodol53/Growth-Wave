import httpx
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from app import models, crud
from app.core.security import decrypt_data
from app.core.config import settings
from app.collectors.base import BaseCollector
from app.schemas.collaboration import CollaborationInteractionCreate
from app.models.collaboration import InteractionType, CollaborationCategory

class JiraCollector(BaseCollector):
    """
    Collects collaboration data from Jira.
    Focuses on recent comments as a primary source of "SUPPORT".
    """
    def collect(self, user: models.User, account: models.external_account.ExternalAccount) -> int:
        if not settings.JIRA_SERVER_URL:
            print("WARNING: JIRA_SERVER_URL is not configured. Skipping Jira collection.")
            return 0

        try:
            credentials = decrypt_data(account.encrypted_credentials)
        except Exception:
            print(f"ERROR: Could not decrypt credentials for user {user.id} and account {account.id}. Skipping.")
            return 0

        print(f"INFO: Starting Jira data collection for user '{user.full_name}' with account '{account.account_id}'")
        
        # 1. Fetch recent comments from Jira API
        # We search for issues where the user has commented in the last 7 days.
        jql = f'comment ~ "{account.account_id}" AND updated >= -7d'
        api_url = f"{settings.JIRA_SERVER_URL}/rest/api/3/search"
        
        headers = {
            "Authorization": f"Bearer {credentials}",
            "Accept": "application/json"
        }
        params = {
            "jql": jql,
            "fields": "comment,assignee,reporter", # Get comments and relevant users
            "expand": "changelog" # To check for assignments if needed
        }

        try:
            with httpx.Client() as client:
                response = client.get(api_url, headers=headers, params=params, timeout=30.0)
                response.raise_for_status()
                issues = response.json().get("issues", [])
        except httpx.HTTPStatusError as e:
            print(f"ERROR: Jira API request failed with status {e.response.status_code} for user {user.id}. Response: {e.response.text}")
            return 0
        except Exception as e:
            print(f"ERROR: An unexpected error occurred during Jira API request for user {user.id}: {e}")
            return 0

        # 2. Transform and save events
        new_interactions_count = 0
        for issue in issues:
            for comment in issue.get("fields", {}).get("comment", {}).get("comments", []):
                # We only care about comments made by the user we are collecting for
                if comment.get("author", {}).get("emailAddress") == account.account_id:
                    transformed_event = self._transform_comment_event(
                        issue=issue,
                        comment=comment,
                        collector_user_id=user.id
                    )
                    if transformed_event:
                        # Here you might want to check if this interaction already exists
                        # For simplicity, we are not doing that now.
                        crud.collaboration.collaboration_interaction.create(self.db, obj_in=transformed_event)
                        new_interactions_count += 1
        
        print(f"INFO: Finished Jira data collection for user '{user.full_name}'. Found {new_interactions_count} new interactions.")
        return new_interactions_count

    def _transform_comment_event(
        self, issue: dict, comment: dict, collector_user_id: int
    ) -> Optional[CollaborationInteractionCreate]:
        """
        Transforms a Jira comment event into a CollaborationInteractionCreate schema.
        A comment is considered "SUPPORT" if the commenter is not the assignee.
        """
        assignee_info = issue.get("fields", {}).get("assignee")
        
        # We can't process if there's no assignee
        if not assignee_info or not assignee_info.get("emailAddress"):
            return None
            
        commenter_email = comment.get("author", {}).get("emailAddress")
        assignee_email = assignee_info.get("emailAddress")

        # Rule: A comment is SUPPORT if the commenter is not the assignee.
        if commenter_email == assignee_email:
            return None

        # Find the target user (the assignee) in our system
        target_user = crud.user.get_by_external_account(
            self.db, provider=models.external_account.Provider.JIRA, account_id=assignee_email
        )
        if not target_user:
            return None # We don't track this interaction if the target user isn't in our system

        # For now, we can't easily determine the project, so we'll use a placeholder.
        # A real implementation would need a mapping from Jira projects to our projects.
        placeholder_project_id = 1 

        try:
            occurred_at = datetime.fromisoformat(comment["created"].replace("Z", "+00:00"))
        except (ValueError, KeyError):
            occurred_at = datetime.utcnow()

        return CollaborationInteractionCreate(
            source_user_id=collector_user_id,
            target_user_id=target_user.id,
            project_id=placeholder_project_id, # Placeholder
            interaction_type=InteractionType.JIRA_COMMENT,
            category=CollaborationCategory.SUPPORT,
            occurred_at=occurred_at
        )