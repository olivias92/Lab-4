# fastapi_app.py
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse

from solitaire import SolitaireGame
from models import User
from models import Game
from models import Score
from models import GameHistory
from models import NewGameForm
from models import GameForm
from models import GameForms
from models import MakeMoveForm
from models import ScoreForm
from models import ScoreForms
from models import UserBestResultForm
from models import UserBestResultForms
from models import GameHistoryForm
from models import GameHistoryForms
from models import StringMessage
from models import Action
from models import StackName
from utils import get_by_urlsafe

from google.cloud import ndb
import jsonpickle

app = FastAPI(
    title="Solitaire Game API",
    version="1.0",
    description="A modern FastAPI version of the Solitaire Game API."
)

# --------------------------
# UTILITY FUNCTIONS
# --------------------------

def to_json(game: SolitaireGame):
    """Convert game data to JSON-serializable dict"""
    return {
        'piles': jsonpickle.encode(game.piles),
        'foundations': jsonpickle.encode(game.foundations),
        'deck': jsonpickle.encode(game.deck),
        'open_deck': jsonpickle.encode(game.open_deck),
        'game_over': game.game_over
    }


def to_python(piles, foundations, deck, open_deck, game_over):
    """Convert stored JSON fields back to SolitaireGame object"""
    return SolitaireGame(
        jsonpickle.decode(piles),
        jsonpickle.decode(foundations),
        jsonpickle.decode(deck),
        jsonpickle.decode(open_deck),
        game_over
    )






# ----- ROUTES -----
@app.post("/user", response_model=StringMessage)
def create_user(request: NewGameForm):
    """
    Create a new user.
    """

    if User.query(User.user_name == request.user_name).get():
        raise HTTPException(status_code=409, detail="User already exists")

    user = User(user_name=request.user_name, email=request.email)
    user.put()
    return StringMessage(message=f"User {request.user_name} created!")




@app.post("/game", response_model=StringMessage)
def new_game(request: NewGameForm):
    """Create a new game"""
    user = User.query(User.user_name == request.user_name).get()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    game = SolitaireGame(None, None, None, None, False)
    game.new_game()

    game_json = to_json(game)

    try:
        game_db = Game.new_game(
            user=user.key,
            piles=game_json['piles'],
            foundations=game_json['foundations'],
            deck=game_json['deck'],
            open_deck=game_json['open_deck']
        )
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail="Failed to create game")

    GameHistory.new_history(
        game=game_db.key,
        sequence=game_db.moves,
        game_over=game_db.game_over,
        piles=game_db.piles,
        foundations=game_db.foundations,
        deck=game_db.deck,
        open_deck=game_db.open_deck
    )

    return game_db.to_form("New game created!")




@app.get("/game", response_model=StringMessage)
def get_game():
    """
    Example endpoint for getting a game.
    """
    return StringMessage(message="Game data would go here!")



# Optional: if running directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_app:app", host="127.0.0.1", port=8000, reload=True)
