import requests
from pydantic import BaseModel


class new_user(BaseModel):
    new_user: str
    email: str | None = None



class new_game(BaseModel):
    current_user: str


class make_move(BaseModel):
    action: str
    origin: str
    destination: str
    card_position: int



class api_model:
    
    def __init__(self, base_url="http://localhost:8000/_ah/api/solitaire/v1"):
        self.base_url = base_url


    def new_user(self, new_user):
        payload = new_user.model_dump()
        resp = requests.post(f"{self.base_url}/game", json=payload)
        return resp.json
        
    
    def get_stack():
        print()
        
        
        
    def new_game(current_user):
        print("")
        
        
    def get_game(game_key):
        print("")
        

    def make_move(game_key, action):
        print("")
        
        
    def cancel_game(game_key):
        print("")
        
        
    def get_scores():
        print("")