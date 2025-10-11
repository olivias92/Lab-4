from typing import List
from pydantic import BaseModel

class ScoreForm(BaseModel):
    user_name: str
    date: str
    moves: int


class ScoreForms(BaseModel):
    """Return multiple ScoreForms"""
    items: List[ScoreForm]
