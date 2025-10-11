from pydantic import BaseModel
from typing import List


class CardForm(BaseModel):
    """CardForm for Card MessageField"""
    suit: str
    number: int
    color: str
    upturned: bool


class CardForms(BaseModel):
    """Return multiple CardForms"""
    cards: List[CardForm]
