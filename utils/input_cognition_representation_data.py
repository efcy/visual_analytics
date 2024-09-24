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


if __name__ == "__main__":
    log_root_path = os.environ.get("VAT_LOG_ROOT")
    client = Vaapi(
        base_url='http://127.0.0.1:8000/',  
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    existing_data = client.logs.list()

    def myfunc(data):
        return data.log_path

    for data in sorted(existing_data, key=myfunc):
        log_id = data.id
        log_path = Path(log_root_path) / data.log_path

        my_parser = Parser()
        my_parser.register("ImageJPEG"   , "Image")
        my_parser.register("ImageJPEGTop", "Image")
        my_parser.register("GoalPerceptTop", "GoalPercept")
        my_parser.register("FieldPerceptTop", "FieldPercept")
        my_parser.register("BallCandidatesTop", "BallCandidates")
        
        game_log = LogReader(str(log_path), my_parser)
        try:
            for frame in tqdm(game_log):
                for repr_name in frame.get_names():
                    if repr_name == "FrameInfo":
                        continue
                    if frame[repr_name] == None:
                        # ScanLineEdgelPercept is empty but we write it anyway to the log
                        continue
                    # we will handle behavior extra in the future
                    if repr_name == "BehaviorStateComplete":
                        continue
                    if repr_name == "BehaviorStateSparse":
                        continue
                    # we already treat images differently, no need to but binary data here in the database
                    if repr_name == "Image" or repr_name == "ImageJPEG":
                        continue
                    if repr_name == "ImageTop" or repr_name == "ImageJPEGTop":
                        continue

                    data = MessageToDict(frame[repr_name])
                    a = client.cognition_repr.create(
                        log_id=log_id, 
                        frame_number=frame['FrameInfo'].frameNumber,
                        representation_name=repr_name,
                        representation_data=data
                    )
        except Exception as e:
            print(repr_name)
            print(f"error parsing the log or inserting it: {e}")
        break
