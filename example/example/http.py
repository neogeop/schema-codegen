from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from example.models.http import UserLogin
from example.models.db import Users, LoginSessions
from example.db import with_db_session
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(user: UserLogin, db_session: Session = Depends(with_db_session)):
    stmt = select(Users).filter(Users.username == user.username)
    result = db_session.execute(stmt)
    user_in_db: Users = result.scalars().first()

    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not pwd_context.verify(user.password, user_in_db.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    login_session = LoginSessions(
        user_id=user_in_db.id,
        created_at=datetime.utcnow() 
    )

    db_session.add(login_session)
    db_session.commit()

    return {"message": "Login successful", "user_id": user_in_db.id}
