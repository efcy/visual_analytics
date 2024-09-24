from pathlib import Path
from typing import Generator, List
from naoth.log import Reader as LogReader
from naoth.log import Parser
from google.protobuf.json_format import MessageToDict
import os
import json
from time import sleep
from tqdm import tqdm
from vaapi.client import Vaapi
import shutil

def copy_file_to_tmp(source_file, target_file=None):
    """
    Copies a file to the system's temporary directory.

    Args:
        source_file (str): The path to the file to be copied.
        target_file (str, optional): The name of the file in the tmp directory. 
            If not provided, the original file name will be used.

    Returns:
        str: The full path to the copied file in the tmp directory.
    """
    tmp_dir = os.getenv("TMPDIR", "/tmp")
    if not target_file:
        target_file = os.path.basename(source_file)
    target_path = os.path.join(tmp_dir, target_file)
    shutil.copy2(source_file, target_path)
    return target_path

if __name__ == "__main__":
    log_root_path = os.environ.get("VAT_LOG_ROOT")
    client = Vaapi(
        base_url='http://127.0.0.1:8000/',  
        api_key="84c6f4b516cc9d292f1b0eba26ea88e99812fbb9",
    )
    existing_data = client.logs.list()

    def myfunc(data):
        return data.log_path

    for data in sorted(existing_data, key=myfunc):
        log_id = data.id
        log_path = Path(log_root_path) / data.log_path
        sensor_log_path = Path(log_root_path) / data.sensor_log_path

        copied_file = copy_file_to_tmp(str(sensor_log_path))
        my_parser = Parser()
        sensor_log = LogReader(str(copied_file), my_parser)
        try:
            for frame in tqdm(sensor_log):
                for repr_name in frame.get_names():
                    if repr_name == "FrameInfo":
                        continue
                    data = MessageToDict(frame[repr_name])
                    """
                    a = client.motion_repr.create(
                        log_id=log_id, 
                        sensor_frame_number=frame['FrameInfo'].frameNumber,
                        sensor_frame_time=frame['FrameInfo'].time,
                        representation_name=repr_name,
                        representation_data=data
                    )
                    """
        except Exception as e:
            print(f"error parsing the log or inserting it: {e}")
        break
