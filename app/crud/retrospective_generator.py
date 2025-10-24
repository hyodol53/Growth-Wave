from datetime import date
from sqlalchemy.orm import Session

from app import crud
from app.core.llm import get_llm_client
from app.models.user import User


def generate_retrospective(db: Session, *, user: User, start_date: date, end_date: date) -> str:
    """
    Generates a retrospective report for a user based on their external account activities.
    """
    external_accounts = crud.external_account.get_external_accounts_by_owner(
        db=db, owner_id=user.id
    )

    if not external_accounts:
        return "No external accounts linked. Please link your Jira or Bitbucket account first."

    # --- This section would be replaced with actual API calls to Jira, Bitbucket, etc. ---
    mock_activities = []
    for account in external_accounts:
        mock_activities.append(
            f"--- Mock activities for {account.account_type.value} account ---"
        )
        mock_activities.append(f"- Resolved ticket PROJECT-123: Fix login bug on {start_date.isoformat()}")
        mock_activities.append(f"- Committed 'feat: Add new dashboard widget' on {end_date.isoformat()}")
        mock_activities.append(f"- Reviewed pull request #456 from a colleague.")

    activity_text = "\n".join(mock_activities)
    # --- End of mock section ---

    prompt = f"Please summarize the following project activities for a retrospective report between {start_date} and {end_date}:\n\n{activity_text}"

    llm_client = get_llm_client()
    summary = llm_client.generate_summary(prompt)

    return summary
