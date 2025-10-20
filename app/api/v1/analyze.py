from fastapi import APIRouter, HTTPException
import pandas as pd

router = APIRouter()

@router.get("/")
async def analyze_transactions():
    try:
        df = pd.read_csv("uploaded_transactions.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.strftime("%Y-%m")

        monthly_sum = df.groupby("Month")["Amount"].sum().reset_index()
        category_sum = df.groupby("Category")["Amount"].sum().reset_index()

        return {
            "monthly": monthly_sum.to_dict(orient="records"),
            "categories": category_sum.to_dict(orient="records"),
            "total": int(df["Amount"].sum())
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="CSV 파일이 업로드되지 않았습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
