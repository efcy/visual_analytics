from .vaapi import vaapi
from requests.auth import HTTPBasicAuth
baseurl = "http://127.0.0.1:8000/api/"
username = "uwer"
password = "tester1"

Hauth = HTTPBasicAuth(username,password)


#example objects
event = {"name":"Mexico"}
patch_event = {"id":10,"name":"México"}

game = {"event":10,"team1":"NaoTH","team2":"Brainstormers"}
patch_game = {"event":10,"team1":"Team Osaka","team2":"Brainstormers"}

log = {"game":8,"player_number":42}

if __name__ == "__main__":
    test =   vaapi(baseurl,Hauth)
    
    #print(test.get_event())
    #print(test.get_event(4))
    #print(test.add_event(event))
    #print(test.change_event(patch_event))
    #id = test.add_games(game)
    #print(test.get_games())
    #print(test.change_games(patch_game,id.get("id")))
    print(test.add_log(log))
    
