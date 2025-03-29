from pydantic import EmailStr
from datetime import datetime, UTC
from sqlmodel import Field, SQLModel
from app.utils.ulid import generate_ulid

class UserBase(SQLModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=100, unique=True)
    username: str = Field(max_length=50, unique=True)
    is_superuser: bool = Field(default=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False
    )

class UserCreate(UserBase):
    password: str = Field(max_length=255)

class User(UserBase, table=True):
    __tablename__ = "users"

    id: str = Field(
        default_factory=generate_ulid,
        primary_key=True,
        max_length=26
    )
    password: str = Field(max_length=255)

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "Daniel",
                "last_name": "Lee",
                "email": "admin@gmail.com",
                "username": "admin",
                "password": "1234567890",
                "is_superuser": True,
                "is_active": True
            }
        }
    }

    def __repr__(self) -> str:
        return f"<User {self.username}>"

class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    username: str = Field(max_length=50)

class UserPublic(UserBase):
    id: str
