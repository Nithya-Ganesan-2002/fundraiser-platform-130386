from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.api import schemas, models, database
from src.api.routes_user import get_current_user

router = APIRouter(prefix="/donations", tags=["donations"])

# PUBLIC_INTERFACE
@router.post("/", response_model=schemas.DonationResponse, summary="Make a donation")
def donate(donation: schemas.DonationCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """Process a donation/payment from current user to campaign."""
    campaign = db.query(models.Campaign).filter(models.Campaign.id == donation.campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found.")
    new_donation = models.Donation(
        user_id=current_user.id,
        campaign_id=donation.campaign_id,
        amount=donation.amount
    )
    campaign.current_amount += donation.amount
    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)
    return new_donation

# PUBLIC_INTERFACE
@router.get("/my", response_model=List[schemas.DonationResponse], summary="My donations")
def read_my_donations(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """Retrieve list of donations made by the current user."""
    return db.query(models.Donation).filter(models.Donation.user_id == current_user.id).all()
