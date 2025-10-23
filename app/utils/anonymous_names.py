import random
from typing import List
from sqlalchemy.orm import Session
from app import crud, models
import datetime

COLORS: List[str] = [
    "빨간", "파란", "노란", "초록", "보라", "주황", "분홍", "하늘색", "남색", "연두색",
    "하얀", "검은", "회색", "갈색", "금색", "은색", "청록색", "진홍색", "크림색", "라임색"
]

ANIMALS: List[str] = [
    "사자", "호랑이", "코끼리", "기린", "하마", "코뿔소", "원숭이", "고릴라", "오랑우탄", "침팬지",
    "판다", "코알라", "캥거루", "펭귄", "북극곰", "물개", "돌고래", "고래", "상어", "악어",
    "거북", "뱀", "도마뱀", "개구리", "두꺼비", "독수리", "매", "부엉이", "참새", "비둘기",
    "강아지", "고양이", "토끼", "햄스터", "다람쥐", "여우", "늑대", "곰", "사슴", "노루",
    "양", "염소", "소", "말", "돼지", "닭", "오리", "거위", "타조", "알파카"
]

def generate_anonymous_name(db: Session, *, praisee_id: int, evaluation_period: str) -> str:
    """
    Generates a unique "Color + Animal" combination for a given praisee in a specific period.
    """
    existing_names_tuples = crud.praise_limiter.get_anonymous_names_for_praisee(
        db, praisee_id=praisee_id, evaluation_period=evaluation_period
    )
    existing_names = {name for name, in existing_names_tuples}
    
    max_attempts = 100 # Failsafe to prevent infinite loops
    for _ in range(max_attempts):
        color = random.choice(COLORS)
        animal = random.choice(ANIMALS)
        new_name = f"{color} {animal}"
        if new_name not in existing_names:
            return new_name
            
    # As a fallback if all combinations are somehow exhausted (highly unlikely)
    return f"특별한 {random.randint(1, 999)}"
