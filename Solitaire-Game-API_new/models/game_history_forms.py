from pydantic import BaseModel
from .card_forms import CardForms
from typing import List


class GameHistoryForm(BaseModel):
    """Return the form representation of the Game History"""
    sequence:int
    game_over:bool
    piles:List[CardForms]
    foundations:List[CardForms]
    deck:List[CardForms]
    open_deck:List[CardForms]


class GameHistoryForms(BaseModel):
    """Return multiple GameHistory Form"""
    items:List[GameHistoryForm]
