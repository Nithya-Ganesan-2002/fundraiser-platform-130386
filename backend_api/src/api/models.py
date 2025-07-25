from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# PUBLIC_INTERFACE
class User(Base):
    """User account model representing an application user."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    name = Column(String(128), nullable=True)
    # relationship fields
    campaigns = relationship("Campaign", back_populates="owner")
    donations = relationship("Donation", back_populates="donor")

# PUBLIC_INTERFACE
class Campaign(Base):
    """Campaign model representing crowdfunding projects."""
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    goal_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(DateTime, server_default=func.now())
    end_date = Column(DateTime)
    image_url = Column(String(256), nullable=True)
    # relationships
    owner = relationship("User", back_populates="campaigns")
    donations = relationship("Donation", back_populates="campaign")

# PUBLIC_INTERFACE
class Donation(Base):
    """Model for donation/payment transactions."""
    __tablename__ = "donations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    amount = Column(Float, nullable=False)
    donated_at = Column(DateTime, server_default=func.now())
    # relationships
    donor = relationship("User", back_populates="donations")
    campaign = relationship("Campaign", back_populates="donations")
