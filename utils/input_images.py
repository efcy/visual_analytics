from naoth.log import Reader as LogReader
from google.protobuf.json_format import MessageToDict
from pathlib import Path
import os
from tqdm import tqdm
from vaapi import client
import json
baseurl = "http://127.0.0.1:8000/api/"
#key can be created on admin site
api_token = os.environ.get("VAT_API_TOKEN")

if __name__ == "__main__":
    # FIXME use environment variables for this
    log_root_path = os.environ.get("VAT_LOG_ROOT")
    my_client = client(baseurl,api_token)
    existing_data = my_client.list_robot_data()

    for data in existing_data:
        robot_data_id = data["id"]
        log_path = Path(log_root_path) / data["log_path"]
        # TODO could we just switch game_logs with extracted in the paths?
        robot_foldername = log_path.parent.name
        game_folder = log_path.parent.parent.parent.name
        extracted_path = log_path.parent.parent.parent / "extracted" / robot_foldername
        # TODO figure out if raw or jpeg dynamically here
        bottom_path = extracted_path / "log_bottom"
        top_path = extracted_path / "log_top"

        bottom_files = Path(bottom_path).glob("*")
        bottom_ar = []
        print(f"inserting bottom data for {game_folder} - {robot_foldername}")
        for idx, file in tqdm(enumerate(bottom_files)):
            framenumber = int(file.stem)
            url_path = str(file).removeprefix(log_root_path).strip("/")

            bottom_ar.append({
                "log": robot_data_id,
                "camera": "BOTTOM",
                "type": "RAW",
                "frame_number": framenumber,
                "image_url": url_path,
            })
            if idx % 50 and idx > 0:
                response = my_client.add_image(bottom_ar)
                bottom_ar.clear()

        top_files = Path(top_path).glob("*")
        top_ar = []
        print(f"inserting top data for {game_folder} - {robot_foldername}")
        for idx, file in tqdm(enumerate(top_ar)):
            framenumber = int(file.stem)
            url_path = str(file).removeprefix(log_root_path).strip("/")
            top_ar.append({
                "log": robot_data_id,
                "camera": "TOP",
                "type": "RAW",
                "frame_number": framenumber,
                "image_url": url_path,
            })
            if idx % 50 and idx > 0:
                response = my_client.add_image(top_ar)
                top_ar.clear()
