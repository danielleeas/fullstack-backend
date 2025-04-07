from sqlmodel import Session, select
from app.models.user import User, UserCreate, UserLogin
from app.core.security import get_password_hash, verify_password

def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def login_user(*, session: Session, user_login: UserLogin) -> User | None:
    statement = select(User).where(User.email == user_login.email)
    session_user = session.exec(statement).first()
    if not session_user:
        return None
    if not verify_password(user_login.password, session_user.password):
        return None
    return session_user