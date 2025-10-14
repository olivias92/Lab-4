from pydantic import BaseModel


class NewGameForm(BaseModel):
    """Form used to send a new game request"""
    user_name: str
