from pydantic import EmailStr, field_validator
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

class UserLogin(SQLModel):
    email: EmailStr = Field(
        max_length=255,
        description="User's email address"
    )
    password: str = Field(
        min_length=8,
        max_length=40,
        description="User's password"
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "password123"
            }
        }
    }

    @field_validator('email')
    def validate_email(cls, v):
        if not v:
            raise ValueError("Email is required")
        return v.lower().strip()

    @field_validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError("Password is required")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(v) > 40:
            raise ValueError("Password must be less than 40 characters")
        return v

class UserPublic(UserBase):
    id: str

class LoginResponse(SQLModel):
    token: str
    user: UserPublic

    model_config = {
        "json_schema_extra": {
            "example": {
                "token": "1234567890",
                "user": {
                    "id": "1234567890",
                    "email": "admin@gmail.com",
                    "username": "admin",
                    "first_name": "Daniel",
                    "last_name": "Lee",
                }
            }
        }
    }
