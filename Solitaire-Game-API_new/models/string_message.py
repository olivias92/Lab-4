from pydantic import BaseModel


class StringMessage(BaseModel):
    """Outbound message"""
    message: str
