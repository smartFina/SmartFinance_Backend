from fastapi import APIRouter, Depends
from datetime import date
from app.services.ai_insights import generate_insights_for_month

router = APIRouter(prefix="/insights", tags=["insights"])

@router.get("/")
def get_insights(month: str, user=Depends(...)):
    # month: "2025-10"
    insights = generate_insights_for_month(user.id, month)
    return {"month": month, "insights": insights}
