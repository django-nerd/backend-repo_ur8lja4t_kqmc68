"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- ContactLead -> "contactlead" collection
- PlanInquiry -> "planinquiry" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class ContactLead(BaseModel):
    """
    Stores website contact requests for sales follow-up
    Collection: contactlead
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    company: Optional[str] = Field(None, description="Company name")
    hashrate: Optional[str] = Field(None, description="Target hashrate e.g., 500 TH/s")
    message: Optional[str] = Field(None, description="Additional details")

class PlanInquiry(BaseModel):
    """
    Stores interest in specific hosting plans
    Collection: planinquiry
    """
    plan: str = Field(..., description="Plan name")
    email: EmailStr = Field(..., description="Contact email")
    notes: Optional[str] = Field(None, description="Notes or requirements")
