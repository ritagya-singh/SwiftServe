from fastapi import HTTPException
raise HTTPException(
    status_code=409,
    detail="Email already exists"
)