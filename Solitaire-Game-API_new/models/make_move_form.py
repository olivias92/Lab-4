from pydantic import BaseModel
from enum import Enum
from typing import Optional


class Action(str, Enum):
    """Enum class for action"""
    MOVE = "MOVE"
    DEAL = "DEAL"
    SHOW = "SHOW"


class StackName(str, Enum):
    """Enum class for stack name"""
    DECK = 1
    FOUNDATION_0 = 2
    FOUNDATION_1 = 3
    FOUNDATION_2 = 4
    FOUNDATION_3 = 5
    PILE_0 = 6
    PILE_1 = 7
    PILE_2 = 8
    PILE_3 = 9
    PILE_4 = 10
    PILE_5 = 11
    PILE_6 = 12


class MakeMoveForm(BaseModel):
    """Form used to submit a make a move request"""
    action: Action = Action.DEAL
    origin: Optional[StackName] = None
    destination: Optional[StackName] = None
    card_position: Optional[int] = None
