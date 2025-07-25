from typing import Optional
from pydantic import BaseModel, EmailStr, constr, Field
from datetime import datetime

# USERS
# PUBLIC_INTERFACE
class UserBase(BaseModel):
    """Base fields for user objects."""
    email: EmailStr

# PUBLIC_INTERFACE
class UserCreate(UserBase):
    """Request schema for new user registration."""
    password: constr(min_length=6)
    name: Optional[str] = None

# PUBLIC_INTERFACE
class UserLogin(BaseModel):
    """Request schema for user authentication."""
    email: EmailStr
    password: str

# PUBLIC_INTERFACE
class UserInDB(UserBase):
    """Internal user model with ID and hashed password."""
    id: int
    name: Optional[str]
    class Config:
        orm_mode = True

# CAMPAIGNS
# PUBLIC_INTERFACE
class CampaignBase(BaseModel):
    """Base campaign attributes."""
    title: str = Field(..., description="Title of the crowdfunding campaign")
    description: Optional[str] = None
    goal_amount: float = Field(..., description="Goal amount to raise")
    end_date: datetime

# PUBLIC_INTERFACE
class CampaignCreate(CampaignBase):
    """Request schema for campaign creation."""
    pass

# PUBLIC_INTERFACE
class CampaignResponse(CampaignBase):
    """Response schema for campaign info."""
    id: int
    current_amount: float
    owner_id: int
    image_url: Optional[str]
    start_date: datetime

    class Config:
        orm_mode = True

# DONATIONS
# PUBLIC_INTERFACE
class DonationCreate(BaseModel):
    """Request schema for creating donations."""
    amount: float
    campaign_id: int

# PUBLIC_INTERFACE
class DonationResponse(BaseModel):
    """Response schema for donation."""
    id: int
    user_id: int
    campaign_id: int
    amount: float
    donated_at: datetime

    class Config:
        orm_mode = True

# GENERAL/ANALYTICS
# PUBLIC_INTERFACE
class AnalyticsResponse(BaseModel):
    """Analytics and progress info for a campaign or user."""
    total_raised: float
    num_donors: int
    progress_percentage: float
