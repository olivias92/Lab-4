from datetime import date
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Session, relationship
from .database import Base, SessionLocal
from .game_forms import GameForm
from .score import Score
from .models_utils import card_deck_objects_to_message_field
from .models_utils import byteify
import json


class Game(Base):
    """Game object"""
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, ForeignKey("user.user_name"), nullable=False)

    moves = Column(Integer, nullable=False, default=0)
    game_over = Column(Boolean, nullable=False, default=False)

    # Store JSON as TEXT (string), similar to NDB.JsonProperty
    piles = Column(Text, nullable=True)
    foundations = Column(Text, nullable=True)
    deck = Column(Text, nullable=True)
    open_deck = Column(Text, nullable=True)
    
    history = relationship("GameHistory", back_populates="game", cascade="all, delete")


    #user = relationship("User", back_populates="games")  # If you have this


    @classmethod
    def new_game(cls, user_name, piles, foundations, deck, open_deck):
        game = Game(
            user_name=user_name,
            moves=0,
            game_over=False,
            piles=piles,
            foundations=foundations,
            deck=deck,
            open_deck=open_deck
        )
        db = SessionLocal()
        db.add(game)
        db.commit()
        db.refresh(game)
        return game

    def save_game(self):
        score = Score(user_name=self.user_name, date=date.today(), moves=self.moves)
        db = SessionLocal()
        db.add(score)
        db.commit()

    def to_form(self, message):
        print("DEBUG to_form values:")
        print("id:", self.id)
        print("moves:", self.moves)
        print("game_over:", self.game_over)
        print("piles:", self.piles)
        print("foundations:", self.foundations)
        print("deck:", self.deck)
        print("open_deck:", self.open_deck)
        
        # Decode JSON strings
        deck_data = byteify(json.loads(self.deck))
        open_deck_data = byteify(json.loads(self.open_deck))
        piles_data = byteify(json.loads(self.piles))
        foundations_data = byteify(json.loads(self.foundations))

        # Extract card lists from py/state
        deck_wrapped = [{"cards": deck_data.get("py/state", {}).get("cards", [])}]
        open_deck_wrapped = [{"cards": open_deck_data.get("py/state", {}).get("cards", [])}]
        piles_wrapped = [{"cards": pile.get("py/state", {}).get("cards", [])} for pile in piles_data]
        foundations_wrapped = [{"cards": foundation.get("py/state", {}).get("cards", [])} for foundation in foundations_data]

        # Convert to Pydantic models
        converted_deck = card_deck_objects_to_message_field(deck_wrapped)
        converted_open_deck = card_deck_objects_to_message_field(open_deck_wrapped)
        converted_piles = card_deck_objects_to_message_field(piles_wrapped)
        converted_foundations = card_deck_objects_to_message_field(foundations_wrapped)

        print("✅ Type of converted_deck:", type(converted_deck))
        print("✅ Type of converted_open_deck:", type(converted_open_deck))

        # Return GameForm
        return GameForm(
            urlsafe_key=str(self.id),
            moves=self.moves or 0,
            game_over=self.game_over or False,
            deck=[converted_deck],
            open_deck=[converted_open_deck],
            piles=converted_piles,
            foundations=converted_foundations,
            message=message
        )
