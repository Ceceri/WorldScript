from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from pydantic import BaseModel
from app.core.llm_integration import generate_event_description, generate_options, generate_ending

router = APIRouter(prefix="/llm", tags=["llm"])

class LLMRequest(BaseModel):
    context: str
    type: str  # "event", "options", "ending"

@router.post("/generate")
def llm_generate(request: LLMRequest, db: Session = Depends(get_db)):
    if request.type == "event":
        return {"description": generate_event_description(request.context)}
    elif request.type == "options":
        return {"options": generate_options(request.context)}
    elif request.type == "ending":
        return {"ending": generate_ending(request.context)}
    else:
        raise HTTPException(status_code=400, detail="Invalid type")
