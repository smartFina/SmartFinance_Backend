from fastapi import APIRouter, UploadFile, File
import pandas as pd
from io import BytesIO

router = APIRouter()

@router.post("/")
async def analyze_csv(file: UploadFile = File(...)):
    """
    거래 내역 CSV를 분석하여 월별·카테고리별 합계 계산
    """
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

    # 날짜 컬럼 추정
    date_col = next((c for c in df.columns if "date" in c.lower() or "날짜" in c), None)
    if not date_col:
        return {"error": "No date column found"}
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])

    # 금액 컬럼 추정
    amount_col = next((c for c in df.columns if "amount" in c.lower() or "금액" in c), None)
    if not amount_col:
        return {"error": "No amount column found"}

    # 카테고리 컬럼 추정
    cat_col = next((c for c in df.columns if "category" in c.lower() or "분류" in c), None)
    if not cat_col:
        df["Category"] = "Uncategorized"
        cat_col = "Category"

    df["Month"] = df[date_col].dt.to_period("M").astype(str)

    monthly = df.groupby("Month")[amount_col].sum().reset_index().to_dict(orient="records")
    category = df.groupby(cat_col)[amount_col].sum().reset_index().to_dict(orient="records")

    return {
        "monthly_summary": monthly,
        "category_summary": category,
        "rows": len(df),
    }
