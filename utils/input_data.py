"""
    This script should put all necessary data from one event into the database
"""
from pathlib import Path
from vaapi import client
import json
import os
import time
import logging
from linetimer import CodeTimer
import subprocess
from datetime import datetime
logging.basicConfig(level=logging.INFO)
baseurl = "http://127.0.0.1:8000/api/"
#key can be created on admin site
api_token = os.environ.get("VAT_API_TOKEN") #"ab43645dd5bc6583cf8b2b9ec4b761728843901c" #
event_list = ["2024-07-15_RC24"]


def handle_games(game):
    # for now we allow only on folder called Experiments to also exist inside the Event folder -> TODO have discussion about additional folders
    
    #print(f"\t{game}")
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

def calculate_images(log_path, robot_data_id):
    with CodeTimer('calculate_images'):
        extracted_path = str(log_path).replace("game_logs", "extracted")

        jpg_bottom_path = Path(extracted_path) / "log_bottom_jpg"
        jpg_top_path = Path(extracted_path) / "log_top_jpg"
        bottom_path = Path(extracted_path) / "log_bottom"
        top_path = Path(extracted_path) / "log_top"

        num_bottom = subprocess.run(f"find {bottom_path} -maxdepth 1 -type f | wc -l", shell=True, capture_output=True, text=True).stdout.strip() if bottom_path.is_dir() else 0
        num_top = subprocess.run(f"find {top_path} -maxdepth 1 -type f | wc -l", shell=True, capture_output=True, text=True).stdout.strip() if top_path.is_dir() else 0
        num_jpg_bottom = subprocess.run(f"find {jpg_bottom_path} -maxdepth 1 -type f | wc -l", shell=True, capture_output=True, text=True).stdout.strip() if jpg_bottom_path.is_dir() else 0
        num_jpg_top = subprocess.run(f"find {jpg_top_path} -maxdepth 1  -type f | wc -l", shell=True, capture_output=True, text=True).stdout.strip() if jpg_top_path.is_dir() else 0

        print(f"\t\tbottom: {num_bottom}")
        print(f"\t\ttop: {num_top}")
        print(f"\t\tbottom jpeg: {num_jpg_bottom}")
        print(f"\t\ttop jpeg: {num_jpg_top}")

        response = my_client.change_robot_data(robot_data_id,log={
            "num_jpg_bottom": int(num_jpg_bottom),
            "num_jpg_top": int(num_jpg_top),
            "num_bottom": int(num_bottom),
            "num_top": int(num_top),
        })
    time.sleep(5)

if __name__ == "__main__":
  log_root_path = os.environ.get("VAT_LOG_ROOT")
  my_client = client(baseurl,api_token)
  
  all_events = [f for f in Path(log_root_path).iterdir() if f.is_dir()]
  for event in sorted(all_events, reverse=True):
      if event.name in event_list:
        response = my_client.add_event({
          "name": event.name,
        })  
        event_id = response["id"]
        
        for game in [f for f in event.iterdir() if f.is_dir()]:
            if str(game.name) == "Experiments":
                print("ignoring Experiments folder")
                continue
            response = handle_games(game)
            game_id = response["id"]
 
            gamelog_path = Path(game) / "game_logs"
            for logfolder in [f for f in gamelog_path.iterdir() if f.is_dir()]:
                #print(f"\t\t{logfolder}")
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
                sensor_log_path = str(Path(logfolder) / "sensor.log").removeprefix(log_root_path).strip("/")
                log_path = str(Path(logfolder) / "combined.log").removeprefix(log_root_path).strip("/")
                if not logfolder.parent.parent.name == "2024-07-20_14-15-00_BerlinUnited_vs_Runswift_half1":
                    continue
                print("aaaaaaaaaaaaaaa", log_path)
                response = my_client.add_robot_data({
                    "game": game_id,
                    "robot_version": version,
                    "player_number": int(playernumber),
                    "head_number": int(head_number),
                    "body_serial": body_serial,
                    "head_serial": head_serial,
                    "representations": data,
                    "sensor_log_path": sensor_log_path,
                    "log_path": log_path,
                })
                print("response", response)
                calculate_images(logfolder, response["id"])