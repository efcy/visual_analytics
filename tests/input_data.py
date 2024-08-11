"""
    This script should put all necessary data from one event into the database
"""
from pathlib import Path
from vaapi import client
import json
import logging,random
from datetime import datetime
logging.basicConfig(level=logging.INFO)
baseurl = "http://127.0.0.1:8000/api/"
#key can be created on admin site
api_token = "514cf2e88eab425cfdfce652994d30a1a0c3b1ad"
event_list = ["2024-07-15_RC24"]

if __name__ == "__main__":
  root_path = "/mnt/q/logs"
  my_client = client(baseurl,api_token)
  

  all_events = [f for f in Path(root_path).iterdir() if f.is_dir()]
  for event in sorted(all_events, reverse=True):
      if event.name in event_list:
        response = my_client.add_event({
          "name": event.name,
        })  
        event_id = response["id"]
        print(event_id)
        
        for game in [f for f in event.iterdir() if f.is_dir()]:
            # for now we allow only on folder called Experiments to also exist inside the Event folder -> TODO have discussion about additional folders
            if str(game.name) == "Experiments":
                print("ignoring Experiments folder")
                continue
            print(f"\t{game}")
            # parse additional information from game folder
            game_parsed = str(game.name).split("_")
            timestamp = game_parsed[0] + "_" + game_parsed[1]
            team1 = game_parsed[2]
            team2 = game_parsed[4]
            halftime = game_parsed[5]

            #TODO add games for the event
            date_object = datetime.strptime(timestamp, "%Y-%m-%d_%H-%M-%S")
            response = my_client.add_games({
              "event": event_id,
              "team1": team1,
              "team2": team2,
              "half": halftime,
              # Hack: by default django return the time with Z appended. We do that on input as well so we can compare it in the add_games function
              "start_time": date_object.isoformat()+ "Z",
            })
