import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional

from database import db, create_document
from schemas import ContactLead, PlanInquiry

app = FastAPI(title="ApexHash API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "ApexHash Backend Running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response

# ------------ API Models for requests (frontend payloads) -------------
class ContactPayload(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    hashrate: Optional[str] = None
    message: Optional[str] = None

class PlanInquiryPayload(BaseModel):
    plan: str
    email: EmailStr
    notes: Optional[str] = None

# ------------------------ API Endpoints -------------------------------
@app.post("/api/contact")
def create_contact(payload: ContactPayload):
    try:
        # validate via Pydantic schema for DB and insert
        lead = ContactLead(**payload.model_dump())
        inserted_id = create_document("contactlead", lead)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/plan-inquiry")
def create_plan_inquiry(payload: PlanInquiryPayload):
    try:
        inquiry = PlanInquiry(**payload.model_dump())
        inserted_id = create_document("planinquiry", inquiry)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
