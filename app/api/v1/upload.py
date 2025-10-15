from fastapi import APIRouter, UploadFile, File
import pandas as pd
from io import BytesIO

router = APIRouter()

@router.post("/")
async def upload_csv(file: UploadFile = File(...)):
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

    # 컬럼 정보와 데이터 일부만 리턴
    return {
        "filename": file.filename,
        "columns": list(df.columns),
        "preview": df.head(5).to_dict(orient="records"),
        "rows": len(df),
    }