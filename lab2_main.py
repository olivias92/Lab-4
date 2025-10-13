# Lab 4 -- Using APIs -- Olivia Smith

import requests
from api_model import api_model, new_user, new_game, make_move


BASE_URL = "http://127.0.0.1:8000"

api = api_model()

print("Console-Line Solitaire\n")
n = 5
print("-" * n)
# Main menu functions




def test_connection():
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
        print("1 ---- Add a New User\n2 ---- New Game\n3 ---- Continue Game\n4 ---- View Scores\n5 ---- Exit Program\n")
        selection = input("Selection: ")
        if selection == "1":
            print("\nYou chose new user!")
            new_user_inter()
        elif selection == "2":
            print("\nYou chose new game!")
            new_game_start()
        elif selection == "3":
            print("\nYou chose continue game!")

        elif selection == "4":
            print("n\nYou chose view scores!")

        elif selection == "5":
            print("")
            break




def new_user_inter():
    
    new_username = input("Plaese enter a username: ")
    email = None
    
    # new_user_info = new_user(new_user=new_username, email = email)
    payload = {"user_name": new_username, "email": email}
    response = requests.post(f"{BASE_URL}/user", json=payload)
    
    #result = api.new_user(new_user_info)
    #print(result)
    if response.status_code == 200 or response.status_code == 201:
        print("User created:", response.json())
    else:
        print("Failed:", response.status_code, response.text)




def game_render_form(stock, waste, foundations, piles):
    # Display for a face down card
    stock_display = "--" if stock else "(empty)"
    
    
    # Display for waste pile
    waste_display = waste[-1] if waste else "(empty)"
    

    # Foundations
    foundation_display = " ".join([f"[{f if f else '--'}]" for f in foundations])
      
    for i, pile in enumerate(piles, start=1):
        print(f"Pile {i}:")
        if not pile:
            print("(empty)")
        else:
            for card in pile:
                print(card)
        print()


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

menu_gen()



"""
def new_user_inter():
    
    while True:
        try:
            new_username = input("Plaese enter a username: ")
            email = None
            
            new_user_info = new_user(new_user=new_username, email = email)
            
            result = api.new_user(new_user_info)
            print(result)
            break
        except(ValueError):
            print("Invalid username: username is already in use. Please enter a different one.")

"""
