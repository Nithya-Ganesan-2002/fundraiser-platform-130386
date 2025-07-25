from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.api import database, models, schemas

router = APIRouter(prefix="/analytics", tags=["analytics"])

# PUBLIC_INTERFACE
@router.get("/campaign/{campaign_id}", response_model=schemas.AnalyticsResponse, summary="Campaign analytics")
def campaign_analytics(campaign_id: int, db: Session = Depends(database.get_db)):
    """Display fundraising progress and analytics for a campaign."""
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    total_raised = campaign.current_amount
    goal = campaign.goal_amount
    progress_percentage = float(total_raised) / goal * 100 if goal > 0 else 0
    num_donors = db.query(models.Donation.user_id).filter(models.Donation.campaign_id == campaign_id).distinct().count()
    return schemas.AnalyticsResponse(
        total_raised=total_raised,
        num_donors=num_donors,
        progress_percentage=progress_percentage
    )
