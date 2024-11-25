from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from example.models.http import UserLogin
from example.models.db import User, LoginSession
from example.db import get_db
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password_hash(username: str, password_hash: str) -> bool: 
    try:
        return pwd_context.verify(username, password_hash)
    except:
        return False

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    stmt = select(User).filter(User.username == user.username)
    result = db.execute(stmt)
    user_in_db: User = result.scalars().first()

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not verify_password_hash(user.password, user_in_db.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    login_session = LoginSession(
        user_id=user_in_db.id,
        created_at=datetime.utcnow() 
    )

    db.add(login_session)
    db.commit()

    return {"message": "Login successful", "user_id": user_in_db.id}
