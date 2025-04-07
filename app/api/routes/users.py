from typing import Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import col, delete, func, select
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.config import settings
from app.models.user import UserPublic, UserRegister, UserCreate
from app.crud import user as user_crud
from app.utils.comon import (
    generate_new_account_email,
    send_email,
    send_email_background,
)

router = APIRouter(tags=["Users"])

@router.get("/me", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user