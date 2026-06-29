from datetime import datetime
from datetime import timedelta
from datetime import timezone

from jose import JWTError
from jose import jwt

from app.config import settings
from app.config import SECRET_KEY
from app.config import ALGORITHM
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

# ==========================================
# Create Access Token
# ==========================================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire
        }
    )

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


# ==========================================
# Verify & Decode JWT
# ==========================================

def verify_access_token(token: str):

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError:

        return None
    
