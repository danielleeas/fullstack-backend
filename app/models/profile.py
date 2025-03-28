from datetime import datetime, UTC
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from app.models.user import User
from app.utils.ulid import generate_ulid

class Profile(SQLModel, table=True):
    __tablename__ = "profiles"

    id: str = Field(
        default_factory=generate_ulid,
        primary_key=True,
        max_length=26
    )
    user_id: str = Field(
        foreign_key="users.id",
        unique=True,
        max_length=26
    )
    bio: Optional[str] = Field(default=None, max_length=500)
    title: Optional[str] = Field(default=None, max_length=100)
    avatar: Optional[str] = Field(default=None, max_length=255)
    cover: Optional[str] = Field(default=None, max_length=255)
    location: Optional[str] = Field(default=None, max_length=100)
    website: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False
    )

    # RelatUserhip (assuming you have a User model)
    user: "User" = Relationship(back_populates="profile")
