"""
    This script calculates the number of exported images in the extracted folder and puts them in the database. 
    THIS IS VERY SLOW WHEN USING THE FILESYSTEM VIA SSHFS
"""
from pathlib import Path
from vaapi.client import Vaapi
import os
import time
import subprocess


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

    response = client.logs.update(
        id=log_id, 
        num_jpg_bottom=int(num_jpg_bottom),
        num_jpg_top=int(num_jpg_top),
        num_bottom=int(num_bottom),
        num_top=int(num_top),
    )
    # SSHFS can get overwhelmed if you run too many queries too fast - wait here a bit
    time.sleep(5)

if __name__ == "__main__":
    log_root_path = os.environ.get("VAT_LOG_ROOT")
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    existing_data = client.logs.list()

    def myfunc(data):
        return data.log_path

    for data in sorted(existing_data, key=myfunc):
        log_id = data.id
        log_path = Path(log_root_path) / data.log_path
        print(log_path)
        total_images = data.num_jpg_bottom + data.num_jpg_top + data.num_bottom + data.num_top
        if total_images == 0:
            calculate_images(log_path.parent, log_id)
        else:
            print("\tNumber of images are already put in the database - we assume that is correct")