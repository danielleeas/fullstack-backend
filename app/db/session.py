from sqlmodel import Session, create_engine, select
from app.core.config import settings
from typing import Generator
from app.models.user import User, UserCreate  # You'll need to import your User model
from app.crud.user import create_user

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)

def init_db() -> None:
    """Initialize the database with a super user if none exists"""
    with Session(engine) as session:
        # Check if any superuser exists
        statement = select(User).where(User.is_superuser == True)
        admin = session.exec(statement).first()
        
        if not admin:
            # Create default superuser
            admin = UserCreate(
                email=settings.ADMIN_EMAIL,
                password=settings.ADMIN_PASSWORD,
                first_name=settings.ADMIN_FIRST_NAME,
                last_name=settings.ADMIN_LAST_NAME,
                username=settings.ADMIN_USERNAME,
                is_superuser=True,
                is_active=True,
            )
            create_user(session=session, user_create=admin)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
