from .card_forms import CardForm, CardForms
import json

def card_deck_objects_to_message_field(objects):
    if not isinstance(objects, list):
        objects = [objects]

    decks = []
    for p in objects:
        if isinstance(p, tuple):
            p = dict([p])
        elif not isinstance(p, dict):
            continue

        cards = []
        for c in p.get("cards", []):
            card_data = c.get("py/state", c)
            card = CardForm(
                suit=card_data.get('suit'),
                number=card_data.get('number'),
                color=card_data.get('color'),
                upturned=card_data.get('upturned')
            )
            cards.append(card)

        decks.append(CardForms(cards=cards))

    return decks if len(decks) > 1 else decks[0]



def byteify(input):
    """Convert JSON string to JSON object"""
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.items()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, str):
        return input
    else:
        return input
