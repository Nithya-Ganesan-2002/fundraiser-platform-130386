from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import models, database
from src.api.routes_user import router as user_router
from src.api.routes_campaign import router as campaign_router
from src.api.routes_donation import router as donation_router
from src.api.routes_analytics import router as analytics_router

app = FastAPI(
    title="Crowdfunding Platform API",
    description="Backend API for crowdfunding application: user/campaign/donations/analytics",
    version="0.1.0",
    openapi_tags=[
        {"name": "users", "description": "User registration, login, and profile"},
        {"name": "campaigns", "description": "Crowdfunding campaign management"},
        {"name": "donations", "description": "Donation/payment processing"},
        {"name": "analytics", "description": "Campaign and user analytics"},
    ],
)

# Enable CORS specifically for the frontend app at http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create all database tables (migrations would be used in production)
models.Base.metadata.create_all(bind=database.engine)

app.include_router(user_router)
app.include_router(campaign_router)
app.include_router(donation_router)
app.include_router(analytics_router)

@app.get("/", tags=["utility"])
def health_check():
    """Health check endpoint for server status."""
    return {"message": "Healthy"}
