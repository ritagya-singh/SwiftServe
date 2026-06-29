from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.authentication.jwt_handler import verify_access_token
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.repositories.user_repository import UserRepository

security = HTTPBearer()

def get_current_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    return payload
    
def get_current_user(
    token=Depends(get_current_token),
    db: Session = Depends(get_db)
):
    repository = UserRepository()

    user = repository.get_user_by_email(
        db,
        token["sub"]
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user