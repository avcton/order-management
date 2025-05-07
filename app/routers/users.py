from app.db.models import User
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.config.database import get_db_session

router = APIRouter()


@router.get("/users")
def get_users(db: Session = Depends(get_db_session)):
    return db.query(User).all()
