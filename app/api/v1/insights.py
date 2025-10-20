from fastapi import APIRouter, HTTPException
import pandas as pd
import google.generativeai as genai
import os

router = APIRouter()

# 환경변수에서 Gemini API 키 가져오기
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@router.get("/")
async def generate_insight():
    try:
        df = pd.read_csv("uploaded_transactions.csv")
        summary = df.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(5)

        prompt = f"""
        다음은 사용자의 최근 소비 내역 요약입니다:
        {summary.to_dict()}
        주요 소비 패턴과 절약 팁을 한국어로 3줄 이내로 요약해주세요.
        """

        model = genai.GenerativeModel("gemini-2.5-flash")
        result = model.generate_content(prompt)
        return {"insight": result.text}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV 파일이 업로드되지 않았습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
