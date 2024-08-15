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


def handle_games(game):
    # for now we allow only on folder called Experiments to also exist inside the Event folder -> TODO have discussion about additional folders
    
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
    return response

def get_robot_version(head_number):
    head_number = int(head_number)

    if head_number > 90:
        return "v5"
    elif head_number < 30:
        return "v6"
    else:
        return "unknown"

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
            if str(game.name) == "Experiments":
                print("ignoring Experiments folder")
                continue
            response = handle_games(game)
            game_id = response["id"]
 
            gamelog_path = Path(game) / "game_logs"
            for logfolder in [f for f in gamelog_path.iterdir() if f.is_dir()]:
                print(f"\t\t{logfolder}")
                logfolder_parsed = str(logfolder.name).split("_")
                playernumber = logfolder_parsed[0]
                head_number = logfolder_parsed[1]
                version = get_robot_version(head_number)
                nao_config_file = Path(logfolder) / "nao.info"
                with open(str(nao_config_file), 'r') as file:
                    # Read all lines from the file
                    lines = file.readlines()

                    # Extract the first and third lines
                    body_serial = lines[0].strip()  # Strip to remove any trailing newline characters
                    head_serial = lines[2].strip()

                representation_file = Path(logfolder) / "representation.json"
                with open(str(representation_file), 'r') as file:
                    # Load the content of the file into a Python dictionary
                    data = json.load(file)

                # FIXME should probably also remove the log folder /mnt/q/logs/
                sensor_log_path = str(Path(logfolder) / "sensor.log").removeprefix("/mnt/q/")
                log_path = str(Path(logfolder) / "combined.log").removeprefix("/mnt/q/")
                response = my_client.add_robot_data({
                    "game": game_id,
                    "robot_version": version,
                    "player_number": playernumber,
                    "head_number": head_number,
                    "body_serial": body_serial,
                    "head_serial": head_serial,
                    "representations": data,
                    "sensor_log_path": sensor_log_path,
                    "log_path": log_path,
                })
