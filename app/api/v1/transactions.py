from fastapi import APIRouter

router = APIRouter()

# 임시 저장용 (나중에 DB 연동 가능)
transactions_data = []

@router.get("/")
def get_transactions():
    """저장된 거래 데이터 조회"""
    return {"transactions": transactions_data, "count": len(transactions_data)}

@router.post("/")
def add_transaction(transaction: dict):
    """새 거래 추가 (MVP용 임시 저장)"""
    transactions_data.append(transaction)
    return {"message": "Transaction added", "count": len(transactions_data)}
