from .card_forms import CardForm, CardForms


def card_deck_objects_to_message_field(objects):
    """Conver Python card deck objects to MessageField"""
    if type(objects) is not list:
        objects = [objects]

    decks = []
    for p in objects:
        cards = []
        cards_list = p.get("cards", [])  # ✅ Safe access
        if "cards" not in p:
            print("⚠️ Missing 'cards' in object:", p)
        for c in cards_list:
            card = CardForm(
                suit=c.get('suit'),
                number=c.get('number'),
                color=c.get('color'),
                upturned=c.get('upturned')
            )
            cards.append(card)

        deck = CardForms(cards=cards)
        decks.append(deck)

    return decks[0] if len(decks) == 1 else decks

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
