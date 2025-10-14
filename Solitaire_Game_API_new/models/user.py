from sqlalchemy import Column, String
from .database import Base


class User(Base):
    """User profile"""
    __tablename__ = "user"  # Explicitly using singular as you requested

    user_name = Column(String, primary_key=True, index=True)  # Username as unique identifier
    email = Column(String, nullable=True)  # Optional / NULL allowed
