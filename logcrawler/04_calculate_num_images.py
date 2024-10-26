"""
    This script calculates the number of exported images in the extracted folder and puts them in the database. 
    THIS IS VERY SLOW WHEN USING THE FILESYSTEM VIA SSHFS
"""
from pathlib import Path
from vaapi.client import Vaapi
import os
import subprocess
import argparse


def calculate_images(log_path, log_id):
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

    response = client.log_status.list(log_id=log_id)
    if len(response) == 0:
        return False
    log_status = response[0]
    print(log_status)
    # TODO do a try catch here
    response = client.log_status.update(
        log_id=log_status.log_id, 
        num_jpg_bottom=int(num_jpg_bottom),
        num_jpg_top=int(num_jpg_top),
        num_bottom=int(num_bottom),
        num_top=int(num_top),
    )
    # SSHFS can get overwhelmed if you run too many queries too fast - wait here a bit
    # TODO only do this when using sshfs
    #time.sleep(5)


def is_done(log_id):
    # get the log status object for a given log_id
    response = client.log_status.list(log_id=log_id)
    print(log_id)
    if len(response) == 0:
        print("\tno log_status found")
        return False
    
    log_status = response[0]
    # if all numbers are zero or null we return false
    total_images = int(log_status.num_jpg_bottom or 0) + int(log_status.num_jpg_top or 0) + int(log_status.num_bottom or 0) + int(log_status.num_top or 0)

    if total_images == 0:
        return False
    else:
        return True


if __name__ == "__main__":
    log_root_path = os.environ.get("VAT_LOG_ROOT")

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force", action="store_true", default=False)
    args = parser.parse_args()

    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    existing_data = client.logs.list()

    def sort_key_fn(data):
        return data.log_path

    for data in sorted(existing_data, key=sort_key_fn):
        log_id = data.id
        log_path = Path(log_root_path) / data.log_path
        print(log_path)

        if is_done(log_id) and not args.force:
            print("\tNumber of images are already put in the database - we assume that it is correct")
        else:
            calculate_images(log_path.parent, log_id)