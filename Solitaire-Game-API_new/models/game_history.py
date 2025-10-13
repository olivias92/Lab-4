from sqlalchemy import Column, Integer, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import SessionLocal, Base
from .game_forms import GameForm
from .game_history_forms import GameHistoryForm
from .models_utils import card_deck_objects_to_message_field, byteify
import json
from typing import Union

class GameHistory(Base):
    """GameHistory object"""
    
    __tablename__ = "game_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    sequence = Column(Integer, nullable=False)
    game_over = Column(Boolean, nullable=False)
    piles = Column(JSON, nullable=False)
    foundations = Column(JSON, nullable=False)
    deck = Column(JSON, nullable=False)
    open_deck = Column(JSON, nullable=False)
    
    game = relationship("Game", back_populates="history")

    @classmethod
    def new_history(cls, game: Union[int, "Game"], sequence, game_over,
                    piles, foundations, deck, open_deck):
  # Determine game_id from the passed value
        if hasattr(game, "id"):
            game_id = game.id
        else:
            game_id = int(game)
            
        session = SessionLocal()
        try:
            history = cls(
                game_id=game_id,
                sequence=sequence,
                game_over=game_over,
                piles=piles,
                foundations=foundations,
                deck=deck,
                open_deck=open_deck
            )
            session.add(history)
            session.commit()
            session.refresh(history)
            return history
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    
    def to_form(self, message):
        print("DEBUG to_form values:")
        print("id:", self.id)
        print("moves:", self.moves)
        print("game_over:", self.game_over)
        print("piles:", self.piles)
        print("foundations:", self.foundations)
        print("deck:", self.deck)
        print("open_deck:", self.open_deck)
        return GameForm(
            urlsafe_key=str(self.id),
            moves=self.moves,
            game_over=self.game_over,
            piles=card_deck_objects_to_message_field(byteify(json.loads(self.piles))),
            foundations=card_deck_objects_to_message_field(byteify(json.loads(self.foundations))),
            deck=card_deck_objects_to_message_field(byteify(json.loads(self.deck))),
            open_deck=card_deck_objects_to_message_field(byteify(json.loads(self.open_deck))),
            message=message
        )
"""
    def to_form(self):
        form = GameHistoryForm()
        form.sequence = self.sequence
        form.game_over = self.game_over
        form.piles = card_deck_objects_to_message_field(
            byteify(json.loads(self.piles)))
        form.foundations = card_deck_objects_to_message_field(
            byteify(json.loads(self.foundations)))
        form.deck = card_deck_objects_to_message_field(
            byteify(json.loads(self.deck)))
        form.open_deck = card_deck_objects_to_message_field(
            byteify(json.loads(self.open_deck)))
        return form
"""