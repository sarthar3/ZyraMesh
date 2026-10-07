from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any

from app.core.security import create_access_token, get_current_user, DEFAULT_USERS

router = APIRouter(prefix="/auth", tags=["Authentication & Security"])

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    username = req.username.strip().lower()
    if username in DEFAULT_USERS:
        user_info = DEFAULT_USERS[username]
    else:
        # Allow instant login with custom username as 'user' role
        user_info = {"user_id": f"usr_{username}", "username": username, "role": "user", "name": req.username.capitalize()}

    token = create_access_token(data={"sub": user_info["username"], "role": user_info["role"], "name": user_info["name"]})
    return TokenResponse(access_token=token, user=user_info)

@router.get("/me")
def get_me(user: Dict[str, Any] = Depends(get_current_user)):
    return user
