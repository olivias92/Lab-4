from pydantic import BaseModel
from typing import Any, Dict


class User(BaseModel):
    user_name: str
    email: None
    
class StringMessage(BaseModel):
    message: str


class Game(BaseModel):
    moves: int
    game_over: bool
    piles: Dict[str, Any]
    foundations: Dict[str, Any]
    deck: Dict[str, Any]
    open_deck: Dict[str, Any]
    
class Score(BaseModel):
    user: str
    
