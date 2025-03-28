from typing import Any
from sqlmodel import SQLModel

class Base(SQLModel):
    """
    Base class for all models, inheriting from SQLModel
    which combines SQLAlchemy and Pydantic functionality
    """
    
    class Config:
        # Allow ORM mode for SQLAlchemy integration
        orm_mode = True
        # Make sure each model has its own table
        table = True
        # Add schema validation
        validate_assignment = True
        # Use field names as-is (don't convert to camelCase)
        alias_generator = None
        # Allow extra fields in the database
        extra = "allow"
        arbitrary_types_allowed = True
        from_attributes = True  # This replaces orm_mode=True in Pydantic v2

    class Meta:
        abstract = True  # This tells SQLModel that this is an abstract base class

    def dict(self) -> dict[str, Any]:
        """
        Convert model instance to dictionary
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
