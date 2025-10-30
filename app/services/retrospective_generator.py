from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app import crud, models
from app.core.llm import generate_retrospective_from_gemini

def format_activity_data_for_llm(user: models.User) -> str:
    """
    Fetches activity data for the user from external sources and formats it for the LLM.
    
    NOTE: This is a placeholder implementation. A real implementation would call
    the Jira/Bitbucket collectors to get real-time data without saving it to the DB.
    For now, we'll use dummy data.
    """
    
    # --- Placeholder Data ---
    completed_issues = [
        {"key": "PROJ-123", "summary": "API 성능 개선"},
        {"key": "PROJ-145", "summary": "로그인 시스템 버그 수정"},
    ]
    
    commits = [
        {"message": "feat(PROJ-123): 캐싱 레이어 추가하여 응답 속도 50% 향상"},
        {"message": "fix(PROJ-145): OAuth2 인증 시 리다이렉트 문제 해결"},
        {"message": "refactor: 중복 코드 제거 및 유틸리티 함수로 분리"},
    ]
    
    comments = [
        {"issue": "PROJ-101", "body": "이 문제의 원인은 A모듈의 설정 오류인 것 같습니다. 제가 수정하겠습니다."},
    ]
    # --- End of Placeholder Data ---
    
    context = f"사용자: {user.full_name}\n\n"
    
    context += "1. 완료한 주요 업무:\n"
    for issue in completed_issues:
        context += f"- {issue['key']}: {issue['summary']}\n"
    
    context += "\n2. 주요 코드 기여 (커밋 메시지):\n"
    for commit in commits:
        context += f"- {commit['message']}\n"
        
    context += "\n3. 문제 해결 및 논의 기여 (코멘트):\n"
    for comment in comments:
        context += f"- 이슈 {comment['issue']}에서 '{comment['body']}' 라고 코멘트함.\n"
        
    return context


def generate_retrospective_draft(db: Session, *, user: models.User) -> str:
    """
    Generates a retrospective draft for a user.
    """
    # 1. Fetch and format activity data
    activity_context = format_activity_data_for_llm(user)
    
    # 2. Generate draft using LLM
    draft = generate_retrospective_from_gemini(activity_context)
    
    return draft
