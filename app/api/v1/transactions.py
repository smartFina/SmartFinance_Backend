from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.services.csv_parser import parse_transactions_csv
from app.db.crud import create_transactions_bulk

router = APIRouter(prefix="/transactions", tags=["transactions"])

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...), user=Depends(...)):
    # 간단한 파일 검증
    if not file.filename.endswith((".csv", ".xls", ".xlsx")):
        raise HTTPException(400, "CSV/Excel 파일을 업로드하세요.")
    rows = await file.read()
    transactions = parse_transactions_csv(rows, filename=file.filename)
    created = create_transactions_bulk(user.id, transactions)
    return {"imported": len(created)}