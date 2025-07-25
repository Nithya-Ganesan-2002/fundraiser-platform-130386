from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from src.api import schemas, models, database
from src.api.routes_user import get_current_user

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

# PUBLIC_INTERFACE
@router.post("/", response_model=schemas.CampaignResponse, summary="Create campaign")
def create_campaign(campaign: schemas.CampaignCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """Create a new crowdfunding campaign."""
    db_campaign = models.Campaign(
        title=campaign.title,
        description=campaign.description,
        goal_amount=campaign.goal_amount,
        current_amount=0,
        owner_id=current_user.id,
        end_date=campaign.end_date
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

# PUBLIC_INTERFACE
@router.get("/", response_model=List[schemas.CampaignResponse], summary="List/search campaigns")
def list_campaigns(
    db: Session = Depends(database.get_db),
    q: Optional[str] = Query(None, description="Search query")
):
    """List or search for campaigns."""
    qry = db.query(models.Campaign)
    if q:
        qry = qry.filter(models.Campaign.title.ilike(f"%{q}%"))
    return qry.all()

# PUBLIC_INTERFACE
@router.get("/{campaign_id}", response_model=schemas.CampaignResponse, summary="Get campaign details")
def campaign_detail(campaign_id: int, db: Session = Depends(database.get_db)):
    """Retrieve single campaign details by ID."""
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found.")
    return campaign
