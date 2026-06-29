from fastapi import APIRouter

from fastapi import Depends

from sqlalchemy.orm import Session

from app.authentication.auth_service import AuthService

from app.dependencies.database_dependency import get_db
from app.schemas.auth_schema import RegisterRequest
from app.schemas.auth_schema import RegisterResponse
from app.schemas.auth_schema import LoginRequest
from app.dependencies.auth_dependency import get_current_token
from app.dependencies.auth_dependency import get_current_user


from app.models.user import User

router = APIRouter(

    prefix="/auth",

    tags=["Authentication"]

)

service = AuthService()


@router.post("/register", response_model=RegisterResponse)

def register(

        request: RegisterRequest,

        db: Session = Depends(get_db)

):

    return service.register(db, request)

@router.post("/login" )

def login(

    request: LoginRequest,

    db: Session = Depends(get_db)

):

    return service.login(
        db,
        request
    )



@router.get("/me")
def me(
    current_user=Depends(get_current_user)
):
    return{
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email
    }