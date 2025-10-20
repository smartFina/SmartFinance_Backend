from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import io

router = APIRouter()

@router.post("/")
async def upload_transactions(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="CSV 파일만 업로드 가능합니다.")
        
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        df.columns = [col.strip() for col in df.columns]
        
        # 데이터 검증
        required_cols = {"Date", "Description", "Category", "Amount"}
        if not required_cols.issubset(df.columns):
            raise HTTPException(status_code=400, detail=f"필수 컬럼 누락: {required_cols - set(df.columns)}")

        # 임시 저장 (DB 대신 메모리)
        df.to_csv("uploaded_transactions.csv", index=False)
        
        return {"message": "파일 업로드 성공", "rows": len(df)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
