# Lab 4 -- Using APIs -- Olivia Smith

import requests
from api_model import api_model, new_user, new_game, make_move


#from Solitaire-Game-API_new.models.make_move_form import StackName
from Solitaire_Game_API_new.models.make_move_form import StackName

#rom models.make_move_form import StackName


BASE_URL = "http://127.0.0.1:8000"

api = api_model()

print("Console-Line Solitaire\n")
n = 5
print("-" * n)
# Main menu functions




def test_connection():
    # Default connection
    url = "http://localhost:8080/_ah/api/solitaire/1/user"
    try:
        response = requests.get({BASE_URL})
        print("Status:", response.status_code)
        print("Response:", response.text)
        payload = {
            "user_name": "Alice",
            "email": "alice@example.com"
        }

        response = requests.post(f"{BASE_URL}/user", json=payload)
        print(response.status_code, response.text)
    except Exception as e:
        print("Connection failed:", e)

test_connection()


def menu_gen():
    selection = True
    while True:
        # Menu options text
        print(f"\nPlease select a menu item to continue or press 5 to exit\n")
        print("1 ---- Add a New User\n2 ---- New Game\n3 ---- Continue Game\n4 ---- View Scores\nE ---- Exit Program\n")
        selection = input("Selection: ")
        if selection == "1":
            print("\nYou chose new user!")
            new_user_inter()
        elif selection == "2":
            print("\nYou chose new game!")
            new_game_user()
        elif selection == "E":
            print("")
            break
        
        # Not ready yet
        """
        elif selection == "3":
            print("\nYou chose continue game!")
            print("\tContinue game is not availiable at this time.\t")
        elif selection == "4":
            print("n\nYou chose view scores!")
            print("\tScore view is not available at this time.\t")
        """            





def new_user_inter():
    
    # Email just won't exist. Isn't needed
    new_username = input("Plaese enter a username: ")
    email = None
    

    payload = {"user_name": new_username, "email": email}
    response = requests.post(f"{BASE_URL}/user", json=payload)
    
    #result = api.new_user(new_user_info)
    #print(result)
    if response.status_code == 200 or response.status_code == 201:
        print("User created:", response.json())
    else:
        print("Failed:", response.status_code, response.text)



# WORKS -- Leaving this for testing reasons and a fall-back
def new_game_start():
    current_user = input("Please enter your username: ")
    
    #data = response.json()
    payload = {"user_name": current_user}
    response = requests.post(f"{BASE_URL}/game", json=payload)
    
    if response.status_code == 200 or response.status_code == 201:
        print("Game created!", response.json())
    else:
        print("Failed:", response.status_code, response.text)
    #return data["urlsafe_game_key"], data["state"]



# GAME START HERE
# Function for the start of a game, based on new_game_start()
def new_game_user():
    current_user = input("Please enter your username: ")
    game_data = new_game_render(current_user)
    if not game_data:
        print("Game data is missing. Cannot start game")
        return
    else:
        print(f"Game data received.\t") #game_data
    game_loop(game_data, current_user)


# Function to get username and call first function
def new_game_render(current_user):  
    response = requests.post(f"{BASE_URL}/game", json={"user_name": current_user})
    if response.status_code == 200 or response.status_code == 201:
        try:
            return response.json()
        except Exception as e:
            print("Failed to parse JSON", e)
            
        print("Game created!", response.json())
    else:
        print("Failed to start game.", response.status_code, response.text)
        return None



# Function to take API card objects and format them in simple terms (ex. S7 --> Spade of 7)
def card_format(card):
    if not card["upturned"]:
        return "[-]"
    suit_layout = {
        "heart": "H",
        "diamond": "D",
        "club": "C",
        "spade": "S"
    }
    
    number_layout = {
        1: "A",
        11: "J",
        12: "Q",
        13: "K"
    }
    
    suit = suit_layout.get(card["suit"], "?")
    number = number_layout.get(card["number"], str(card["number"]))
    return f"[{suit}{number}]"



# Function for the foundations
def foundation_render(foundations):
    print("Foundations:\t", end="")
    for pile in foundations:
        if pile["cards"]:
            top_card = pile["cards"][-1]
            print(card_format(top_card), end="\t")
        else:
            print("[--]", end="\t")
    print()



# Function for the piles
def pile_render(piles):
    max_height = max((len(pile["cards"]) for pile in piles), default=0)
    print("\nPiles:\n")
    print("\t" + "\t".join(f"[{i}]" for i in range(len(piles))))

    for row in range(max_height):
        line = ""
        for pile in piles:
            if row < len(pile["cards"]):
                card = pile["cards"][row]
                symbol = card_format(card)
            else:
                symbol = ""
            line += "\t" + symbol
        print(line)



# Function for waste
def waste_render(deck, open_deck):
    draw_count = len(deck[0]["cards"]) if deck else 0
    if open_deck and open_deck[0]["cards"]:
        top_card = open_deck[0]["cards"][-1]
        waste_display = card_format(top_card)
    else:
        waste_display = "[--]"
    print(f"\nWaste:\t{draw_count}\t{waste_display}")


    


# Function to render full game
def game_render_full(game_info, current_user):
    print(f"\tNow playing as: {current_user}")
    
    foundation_render(game_info["foundations"])
    pile_render(game_info["piles"])
    waste_render(game_info["deck"], game_info["open_deck"])
    
    print(f"\nMoves: {game_info["moves"]}")
    print(f"Message: {game_info["message"]}")
    
    
    
# Function to maintain game loop
def game_loop(game_info, current_user):
    print()
    while True:
        game_render_full(game_info, current_user)
        
        while True:
            try:
                action = input("Enter an action to perform (Move/Draw/Show/Cancel): ").strip().lower()
                break
            except(ValueError):
                print("Invalid action passed. Please enter a valid action.\t")
    
       
        
        # Elif and logic for draw action
        if action == "draw":
            try:
                response = requests.put(
                f"{BASE_URL}/game/{game_info['urlsafe_key']}",
                json={
                    "action": "DEAL",
                    "origin": None,
                    "destination": None,
                    "card_position": None
                })
            
                response.raise_for_status()
                game_info = requests.get(f"{BASE_URL}/game/{game_info['urlsafe_key']}").json()
                
            except requests.exceptions.RequestException as e:
                print("Draw failed:", e)

        
        # Elif and logic for move action
        elif action == "move":            
            # Error handling for all the prompts
            while True:
                try:
                    og_pile = input("From what pile would you like to move (PILE_#)? ") 
                    if og_pile in StackName.__members__:
                        origin = StackName[og_pile.strip().upper()]
                        break
                    else:
                        raise ValueError                       
               
                except(ValueError):
                    print("Please enter a valid value.")
                    
                    
            # Destination pile
            while True:
                try:
                    dest_pile = input("Where would you like to put the card (PILE_#, FOUNDATION_#)? ")
                    if dest_pile in StackName.__members__:
                        destination = StackName[dest_pile]
                        break
                    else:
                        raise ValueError
                except(ValueError):
                    print("Please enter a valid value.")
                    
            # Card position 
            while True:
                try:
                    card_post = input("Please enter a card position (Type -1 to move only one card): ")
                    break
                except(ValueError):
                    print("Please enter a valid value.")
                    
                
            # Defaults to -1, or one card position
            card_post = int(card_post) if card_post else -1     

            try:
                response = requests.put(
                f"{BASE_URL}/game/{game_info['urlsafe_key']}",
                json={
                    "action": "MOVE",
                    "origin": origin.value,
                    "destination": destination.value,
                    "card_position": card_post
                })
            
                response.raise_for_status()
                game_info = requests.get(f"{BASE_URL}/game/{game_info['urlsafe_key']}").json()
                
            except requests.exceptions.RequestException as e:
                print("Move failed:", e)
                
                
                
         # Elif and logic for show action
        elif action == "show":
            
            
            while True:
                try:
                    og_pile_show = input("Enter pile number to show card (PILE_#): ").strip().upper()
                    if og_pile_show in StackName.__members__:
                        origin = StackName[og_pile.strip().upper()]
                        break
                    else:
                        raise ValueError                       
               
                except(ValueError):
                    print("Please enter a valid value.")
                    
                    
          
            
            origin_show = StackName[og_pile_show]
            try:
                response = requests.put(
                f"{BASE_URL}/game/{game_info['urlsafe_key']}",
                json={
                    "action": "SHOW",
                    "origin": origin_show.value,
                    "destination": None,
                    "card_position": None
                })
            
                response.raise_for_status()
                game_info = requests.get(f"{BASE_URL}/game/{game_info['urlsafe_key']}").json()
                
            except requests.exceptions.RequestException as e:
                print("Show failed:", e)

        elif action == "cancel":
            print("Game canceled. Returning to main menu.")
            break
    


# Main function call
menu_gen()
