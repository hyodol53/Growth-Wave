import google.generativeai as genai
from app.core.config import settings

def generate_retrospective_from_gemini(context: str) -> str:
    """
    Generates a retrospective draft using the Google Gemini Pro model.
    """
    if not settings.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not configured.")

    try:
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = (
            "당신은 IT 전문가의 업무 회고록을 작성하는 전문 AI 비서입니다. "
            "다음은 특정 기간 동안 한 사용자의 활동 내역입니다. 이 내용을 바탕으로, "
            "주요 성과, 문제 해결 경험, 동료와의 협업, 개인적인 성장 등의 항목으로 나누어 "
            "전문적이고 체계적인 회고록 초안을 작성해 주세요. 각 항목은 구체적인 사례를 기반으로 서술해 주세요.\n\n"
            "--- 활동 내역 ---\n"
            f"{context}"
            "\n--- 회고록 초안 ---"
        )
        
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        # In a real application, you would want more specific error handling
        print(f"ERROR: An error occurred while generating text with Gemini: {e}")
        raise  # Re-raise the exception to be handled by the API layer