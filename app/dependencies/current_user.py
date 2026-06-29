from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_token

from app.repositories.user_repository import UserRepository


repository = UserRepository()


def get_current_user(

    token: dict = Depends(get_current_token),

    db: Session = Depends(get_db)

):

    email = token.get("sub")

    if email is None:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Invalid token."

        )

    user = repository.get_user_by_email(

        db,

        email

    )

    if user is None:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="User not found."

        )

    return user