from pathlib import Path
from typing import Generator, List
import os
from time import sleep
from tqdm import tqdm
from vaapi.client import Vaapi

if __name__ == "__main__":
    print(os.getpid())
    log_root_path = os.environ.get("VAT_LOG_ROOT")
    client = Vaapi(
        base_url='http://127.0.0.1:8000/',  
        api_key="84c6f4b516cc9d292f1b0eba26ea88e99812fbb9",
    )
    existing_data = client.list_robot_data() # FIXME

    def myfunc(data):
        return data["log_path"]

    for data in sorted(existing_data, key=myfunc):
        robot_data_id = data["id"]
        log_path = Path(log_root_path) / data["log_path"]