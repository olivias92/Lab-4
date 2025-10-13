"""utils.py - File for collecting general utility functions."""

import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def get_by_urlsafe(db: Session, model, entity_id):

    entity = db.query(model).get(entity_id)
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found."
        )
    return entity


# === SERIALIZATION HELPERS ===

def card_to_str(card):
    if not card.upturned:
        return "--"
    value_str = {1:"A", 11:"J", 12:"Q", 13:"K"}.get(card.number, str(card.number))
    suit_str = {"heart":"H", "diamond":"D", "club":"C", "spade":"S"}[card.suit]
    return f"{value_str}{suit_str}"

def serialize_pile(pile):
    return [card_to_str(card) for card in pile.cards]

def serialize_game(game):
    return {
        "deck": [card_to_str(c) for c in game.deck.cards],
        "open_deck": [card_to_str(c) for c in game.open_deck.cards],
        "foundations": [serialize_pile(f) for f in game.foundations],
        "piles": [serialize_pile(p) for p in game.piles],
        "game_over": game.game_over
    }