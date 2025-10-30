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

def get_anonymous_name_for_praise(praise_id: int, adjective_list: list[str], animal_list: list[str]) -> str:
    """
    Generates a deterministic anonymous name combining an adjective and an animal
    based on the praise ID.
    """
    if not adjective_list or not animal_list:
        return "익명의 누군가"
    
    selected_adjective = adjective_list[praise_id % len(adjective_list)]
    # Use a different calculation for the animal to ensure variety
    selected_animal = animal_list[(praise_id // len(adjective_list)) % len(animal_list)]
    
    return f"익명의 {selected_adjective} {selected_animal}"
