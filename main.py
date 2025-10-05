# Lab 4 -- Using APIs -- Olivia Smith

import requests
from api_model import api_model, new_user, new_game, make_move

BASE_URL = "http://localhost:8000/_ah/api/solitaire/v1"

api = api_model()

print("Console-Line Solitaire\n")
n = 5
print("-" * n)
# Main menu functions

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
    
    new_user_info = new_user(new_user=new_username, email = email)
    
    result = api.new_user(new_user_info)
    print(result)






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

menu_gen()
