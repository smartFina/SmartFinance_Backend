from fastapi import APIRouter, UploadFile, File
import pandas as pd
from io import BytesIO

router = APIRouter()

@router.post("/")
async def upload_csv(file: UploadFile = File(...)):
    """
    CSV/Excel 파일을 업로드하고 컬럼 및 미리보기 데이터 반환
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

    return {
        "filename": file.filename,
        "columns": list(df.columns),
        "preview": df.head(5).to_dict(orient="records"),
        "rows": len(df),
    }
