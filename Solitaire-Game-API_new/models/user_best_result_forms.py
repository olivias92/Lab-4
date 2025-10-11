from pydantic import BaseModel
from typing import List


class UserBestResultForm(BaseModel):
    """Form for outbound User best result information"""
    user: str
    least_moves: int


class UserBestResultForms(BaseModel):
    """Return multiple UserBestResultForm"""
    items: List[UserBestResultForm]
