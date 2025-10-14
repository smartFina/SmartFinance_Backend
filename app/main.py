# app/main.py
from fastapi import FastAPI

app = FastAPI(title="SmartFinance API", version="0.1")

@app.get("/")
def root():
    return {"message": "SmartFinance API is running 🚀"}

# 추가: 개발 확인용 라우터 (예: /ping)
@app.get("/ping")
def ping():
    return {"status": "ok"}
