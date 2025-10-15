# app/api/analyze.py
from fastapi import APIRouter, UploadFile, File
import pandas as pd
from io import BytesIO

router = APIRouter()

@router.post("/")
async def analyze_csv(file: UploadFile = File(...)):
    """
    거래 내역 CSV를 업로드받아 월별·카테고리별 통계를 계산
    """

    # 파일 검사
    if not file.filename.endswith((".csv", ".xls", ".xlsx")):
        return {"error": "Only CSV or Excel files are supported"}

    content = await file.read()
    try:
        if file.filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(content))
        else:
            df = pd.read_excel(BytesIO(content))
    except Exception as e:
        return {"error": str(e)}

    # ====== ⚙️ 데이터 전처리 ======
    # 날짜 컬럼 이름 유추
    date_col = None
    for c in df.columns:
        if "date" in c.lower() or "날짜" in c:
            date_col = c
            break
    if date_col is None:
        return {"error": "No date column found"}

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])

    # 금액 컬럼 찾기
    amount_col = None
    for c in df.columns:
        if "amount" in c.lower() or "금액" in c:
            amount_col = c
            break
    if amount_col is None:
        return {"error": "No amount column found"}

    # 카테고리 컬럼 찾기 (없으면 'Uncategorized'로 처리)
    cat_col = None
    for c in df.columns:
        if "category" in c.lower() or "분류" in c:
            cat_col = c
            break
    if cat_col is None:
        df["Category"] = "Uncategorized"
        cat_col = "Category"

    # ====== 📊 통계 계산 ======
    df["Month"] = df[date_col].dt.to_period("M").astype(str)

    # 월별 합계
    monthly = df.groupby("Month")[amount_col].sum().reset_index().to_dict(orient="records")

    # 카테고리별 합계
    category = df.groupby(cat_col)[amount_col].sum().reset_index().to_dict(orient="records")

    # ====== 🔁 결과 반환 ======
    return {
        "monthly_summary": monthly,
        "category_summary": category,
        "rows": len(df),
    }
