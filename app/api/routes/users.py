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

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signup", response_model=UserPublic)
def register_user(session: SessionDep, user_in: UserRegister, background_tasks: BackgroundTasks) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = user_crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.model_validate(user_in)
    user = user_crud.create_user(session=session, user_create=user_create)
    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        send_email_background(
            background_tasks,
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return user