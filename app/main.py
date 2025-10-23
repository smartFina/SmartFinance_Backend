from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.v1 import upload, analyze, transactions, insights

load_dotenv()
app = FastAPI(title="SmartFinance API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api/upload", tags=["Upload"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["Analyze"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["Transactions"])
app.include_router(insights.router, prefix="/api/insights", tags=["Insights"])

@app.get("/")
def root():
    return {"message" : "SmartFinance API is running..."}