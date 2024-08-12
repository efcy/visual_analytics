from naoth.log import Reader as LogReader
from google.protobuf.json_format import MessageToDict
from pathlib import Path
from tqdm import tqdm
from vaapi import client
import json
baseurl = "http://127.0.0.1:8000/api/"
#key can be created on admin site
api_token = "514cf2e88eab425cfdfce652994d30a1a0c3b1ad"

if __name__ == "__main__":
    # FIXME use environment variables for this
    root_path = "/mnt/q/"
    my_client = client(baseurl,api_token)
    existing_data = my_client.list_robot_data()

    for data in existing_data:
        robot_data_id = data["id"]
        log_path = Path(root_path) / data["log_path"]
        # TODO could we just switch game_logs with extracted in the paths?
        robot_foldername = log_path.parent.name
        game_folder = log_path.parent.parent.parent.name
        

        if not game_folder == "2024-07-15_20-00-00_BerlinUnited_vs_SPQR_half1-test":
            break

        extracted_path = log_path.parent.parent.parent / "extracted" / robot_foldername
        bottom_path = extracted_path / "log_bottom"
        top_path = extracted_path / "log_top"
        bottom_files = Path(bottom_path).glob("*")
        for file in tqdm(bottom_files):
            framenumber = int(file.stem)
            url_path = str(file).removeprefix("/mnt/q/logs/")
            response = my_client.add_image({
                "log": robot_data_id,
                "camera": "BOTTOM",
                "type": "RAW",
                "frame_number": framenumber,
                "image_url": url_path,
            })
        break