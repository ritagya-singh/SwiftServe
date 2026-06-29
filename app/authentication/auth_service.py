from sqlalchemy.orm import Session

from app.authentication.password import hash_password

from app.models.user import User

from app.repositories.user_repository import UserRepository

from app.authentication.password import verify_password
from app.authentication.jwt_handler import create_access_token


class AuthService:

    def __init__(self):

        self.repository = UserRepository()

    def register(self, db: Session, data):

        existing = self.repository.get_user_by_email(
            db,
            data.email
        )

        if existing:

            raise Exception("Email already exists")

        new_user = User(

            name=data.name,

            email=data.email,

            password=hash_password(data.password)

        )

        return self.repository.create_user(db, new_user)
    
    def login(self, db: Session, request):

        user = self.repository.get_user_by_email(
        db,
        request.email
    )

        if not user:

            raise Exception("Invalid Email")

        if not verify_password(
            request.password,
            user.password
    ):

            raise Exception("Invalid Password")

        token = create_access_token(

            {
                 "sub": user.email
            }

        )

        return {

            "access_token": token,

            "token_type": "Bearer"

        }