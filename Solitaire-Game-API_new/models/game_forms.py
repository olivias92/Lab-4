from pydantic import BaseModel
from typing import List
from .card_forms import CardForms


class GameForm(BaseModel):
    """GameForm for outbound game state information"""
    urlsafe_key: str
    moves: int
    game_over: bool
    piles: List[CardForms]
    foundations: List[CardForms]
    deck: List[CardForms]
    open_deck: List[CardForms]
    message: str


class GameForms(BaseModel):
    """Return multiple GameForms"""
    items: List[GameForm]
