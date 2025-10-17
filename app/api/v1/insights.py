from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.config import GEMINI_API_KEY
import google.generativeai as genai

router = APIRouter()

genai.configure(api_key=GEMINI_API_KEY)

class InsightRequest(BaseModel):
    monthly_summary: list
    category_summary: list

@router.post("/")
async def generate_insight(data: InsightRequest):
    """
    Google Gemini API를 사용해 소비 분석 인사이트 생성
    """
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key not configured")

    prompt = f"""
    다음은 사용자의 지출 데이터입니다.

    [월별 지출 요약]
    {data.monthly_summary}

    [카테고리별 지출 요약]
    {data.category_summary}

    위 데이터를 기반으로 사용자의 소비 습관을 분석하고,
    - 주된 소비 패턴
    - 지출이 늘어난 이유 추정
    - 절약 팁 2가지
    를 간결하고 자연스럽게 요약해줘.
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return {"insight": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
