# fastapi_app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Solitaire Game API",
    version="1.0",
    description="A modern FastAPI version of the Solitaire Game API."
)

# ----- MODELS -----
class NewUser(BaseModel):
    user_name: str
    email: Optional[str] = None

class StringMessage(BaseModel):
    message: str


# ----- ROUTES -----
@app.post("/user", response_model=StringMessage)
def create_user(user: NewUser):
    """
    Create a new user.
    """

    # Simulate checking if user exists (replace with DB call later)
    if user.user_name.lower() == "test":
        raise HTTPException(status_code=409, detail="User already exists")

    return StringMessage(message=f"User {user.user_name} created!")


@app.get("/game", response_model=StringMessage)
def get_game():
    """
    Example endpoint for getting a game.
    """
    return StringMessage(message="Game data would go here!")


@app.post("/game", response_model=StringMessage)
def new_game():
    """
    Example endpoint for creating a game.
    """
    return StringMessage(message="New game created!")


# Optional: if running directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_app:app", host="127.0.0.1", port=8000, reload=True)
