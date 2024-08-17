from pathlib import Path
from typing import Generator, List
import os
from time import sleep
from tqdm import tqdm

from vaapi import client
baseurl = "http://127.0.0.1:8000/api/"
#key can be created on admin site
api_token = os.environ.get("VAT_API_TOKEN")

def scandir_yield_files(directory):
    """Generator that yields file paths in a directory."""
    with os.scandir(directory) as it:
        for entry in it:
            if entry.is_file():
                yield entry.path

def path_generator(directory: str, batch_size: int = 100) -> Generator[List[str], None, None]:
    batch = []
    for path in scandir_yield_files(directory):
        batch.append(path)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

def handle_insertion(individual_extracted_folder, data, camera, type):

    print(individual_extracted_folder)
    if not Path(individual_extracted_folder).is_dir():
        return
    if check_insertion(robot_data_id, camera, type):
        return

    

    for batch in path_generator(individual_extracted_folder):
        image_ar = [None] * len(batch)
        for idx, file in enumerate(batch):

            framenumber = int(Path(file).stem)
            url_path = str(file).removeprefix(log_root_path).strip("/")
            
            image_ar[idx] = {
                "log": robot_data_id,
                "camera": camera,
                "type": type,
                "frame_number": framenumber,
                "image_url": url_path,
            }

        response = my_client.add_image(image_ar)

        sleep(0.5)
    sleep(5)

def check_insertion(robot_data_id, camera, type):
    # TODO get the number of images in db via api => write an endpoint for this
    params = {
        "log": robot_data_id,
        "camera": camera,
        "type": type,
    }
    response = my_client.image_count(params)
    db_count = int(response["count"])
    

    response2 = my_client.get_robot_data(robot_data_id)
    if camera == "BOTTOM" and type == "RAW":
        target_count = int(response2["num_bottom"])
    elif camera == "TOP" and type == "RAW":
        target_count = int(response2["num_top"])
    elif camera == "BOTTOM" and type == "JPEG":
        target_count = int(response2["num_jpg_bottom"])
    elif camera == "TOP" and type == "JPEG":
        target_count = int(response2["num_jpg_top"])
    else:
        ValueError()

    if target_count == db_count:
        print("\tskipping insertion")
        return True

    return False


if __name__ == "__main__":
    print(os.getpid())
    log_root_path = os.environ.get("VAT_LOG_ROOT")
    my_client = client(baseurl,api_token)
    existing_data = my_client.list_robot_data()

    def myfunc(data):
        return data["log_path"]

    for data in sorted(existing_data, key=myfunc):
        robot_data_id = data["id"]
        log_path = Path(log_root_path) / data["log_path"]


        # TODO could we just switch game_logs with extracted in the paths?
        robot_foldername = log_path.parent.name
        game_folder = log_path.parent.parent.parent.name
        extracted_path = log_path.parent.parent.parent / "extracted" / robot_foldername
        # TODO figure out if raw or jpeg dynamically here
        print(f"inserting bottom data for {game_folder} - {robot_foldername}")
        bottom_path = extracted_path / "log_bottom"
        top_path = extracted_path / "log_top"
        bottom_path_jpg = extracted_path / "log_bottom_jpg"
        top_path_jpg = extracted_path / "log_top_jpg"

        handle_insertion(bottom_path, data, camera="BOTTOM", type="RAW")
        handle_insertion(top_path, data, camera="TOP", type="RAW")
        handle_insertion(bottom_path_jpg, data, camera="BOTTOM", type="JPEG")
        handle_insertion(top_path_jpg, data, camera="TOP", type="JPEG")
        break