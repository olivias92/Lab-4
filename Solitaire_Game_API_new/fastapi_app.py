# fastapi_app.py
import logging
import os
os.environ["DATASTORE_EMULATOR_HOST"] = "localhost:8081"
os.environ["DATASTORE_DATASET"] = "test-project"
os.environ["DATASTORE_PROJECT_ID"] = "test-project"

from sqlalchemy.orm import Session
from models.database import Base, engine, SessionLocal
from models.user import User
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from solitaire import SolitaireGame
from models.user import User
from models.game import Game
from models.score import Score
from models.game_history import GameHistory
from models.new_game_form import NewGameForm
from models.game_forms import GameForm
from models.game_forms import GameForms
from models.make_move_form import MakeMoveForm
from models.score_forms import ScoreForm
from models.score_forms import ScoreForms
from models.user_best_result_forms import UserBestResultForm
from models.user_best_result_forms import UserBestResultForms
from models.game_history_forms import GameHistoryForm
from models.game_history_forms import GameHistoryForms
from models.string_message import StringMessage
from models.make_move_form import Action
from models.make_move_form import StackName

Base.metadata.create_all(bind=engine)

from fastapi import FastAPI, HTTPException, Depends
from utils import get_by_urlsafe, card_to_str, serialize_pile, serialize_game

from google.cloud import ndb
import jsonpickle

app = FastAPI(
    title="Solitaire Game API",
    version="1.0",
    description="A modern FastAPI version of the Solitaire Game API."
)

# Consts




ndb_client = ndb.Client(project="test-project", credentials=None)

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



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
class UserCreate(BaseModel):
    user_name: str
    email: str | None = None
    


# ----- ROUTES -----
@app.post("/user", response_model=StringMessage)
def create_user(request: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.user_name == request.user_name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(user_name=request.user_name, email=request.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created", "user": {"user_name": new_user.user_name, "email": new_user.email}}


@app.get("/user/{user_name}")
def get_user(user_name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_name == user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_name": user.user_name, "email": user.email}



# GAME ROUTES
@app.post("/game", response_model=GameForm)
def new_game(request: NewGameForm, db: Session = Depends(get_db)):
    """Create a new game"""
    user = db.query(User).filter(User.user_name == request.user_name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    game = SolitaireGame(None, None, None, None, False)
    game.new_game()

    game_json = to_json(game)

    try:
        game_db = Game.new_game(
            user_name=user.user_name,
            piles=game_json['piles'],
            foundations=game_json['foundations'],
            deck=game_json['deck'],
            open_deck=game_json['open_deck']
        )
    except Exception as e:
        logging.error(str(e))
        raise HTTPException(status_code=500, detail="Failed to create game")

    GameHistory.new_history(
        game=game_db.id,
        sequence=game_db.moves,
        game_over=game_db.game_over,
        piles=game_db.piles,
        foundations=game_db.foundations,
        deck=game_db.deck,
        open_deck=game_db.open_deck
    )
    #return JSONResponse(serialize_game(game))
    return game_db.to_form("New game created!")



# Get game
@app.get("/game/{urlsafe_game_key}", response_model=GameForm)
def get_game(urlsafe_game_key: str, db: Session = Depends(get_db)):
    """Return current game state"""
    game = get_by_urlsafe(db, Game, urlsafe_game_key)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game.to_form("Time to make a move!")




# Make move
@app.put("/game/{urlsafe_game_key}", response_model=GameForm)
def make_move(urlsafe_game_key: str, request: MakeMoveForm, db: Session = Depends(get_db)):
    """Make a move"""
    game_db = get_by_urlsafe(db, Game, urlsafe_game_key)
    if not game_db:
        raise HTTPException(status_code=404, detail="Game not found")

    if game_db.game_over:
        return game_db.to_form("Game already over")

    game = to_python(game_db.piles, game_db.foundations, game_db.deck,
                    game_db.open_deck, game_db.game_over)

    action = request.action
    origin = request.origin
    destination = request.destination
    card_position = request.card_position or -1

    changed = False

    if action == Action.DEAL:
        game.deal()
        changed = True
        game_db.moves += 1
        game_db.moves = game.moves

    elif action == Action.MOVE:
        if not origin or not destination:
            raise HTTPException(status_code=400, detail="Origin and destination required")
        
        origin = origin.name
        destination = destination.name
        changed = game.move(origin=str(origin), destination=str(destination),
                            card_position=card_position)
        if not changed:
            raise HTTPException(status_code=400, detail="Illegal move")
        if changed:
            game_db.moves += 1
            game_db.moves = game.moves

    elif action == Action.SHOW:
        if not origin:
            raise HTTPException(status_code=400, detail="Origin required for SHOW action")
        changed = game.show_top(origin.name)
        game_db.moves += 1
        game_db.moves = game.moves
        if not changed:
            raise HTTPException(status_code=400, detail="Could not show card")
        if changed:
            game_db.moves += 1
            game_db.moves = game.moves
            
    # Save updates
    if changed:
        game_json = to_json(game)
        game_db.piles = game_json['piles']
        game_db.foundations = game_json['foundations']
        game_db.deck = game_json['deck']
        game_db.open_deck = game_json['open_deck']
        game_db.game_over = game_json['game_over']
        db.commit()

        GameHistory.new_history(
            game=game_db.id,
            sequence=game_db.moves,
            game_over=game_db.game_over,
            piles=game_db.piles,
            foundations=game_db.foundations,
            deck=game_db.deck,
            open_deck=game_db.open_deck
        )

    if game_db.game_over:
        game_db.save_game()

    return game_db.to_form("Made a move")

"""

# Cancel Game
@app.delete("/game/{game_id}")
def cancel_game(game_id: str):
    

# Get Scores



@app.get("/")
def root():
    return {"message": "Solitaire API is running!"}

"""

# Optional: if running directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_app:app", host="127.0.0.1", port=8000, reload=True)
    

