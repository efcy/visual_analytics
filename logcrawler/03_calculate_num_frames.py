from pathlib import Path
from naoth.log import Reader as LogReader
from naoth.log import Parser
import os
from vaapi.client import Vaapi
from tqdm import tqdm

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
        sensor_log_path = Path(log_root_path) / data.sensor_log_path

        my_parser = Parser()
        my_parser.register("ImageJPEG"   , "Image")
        my_parser.register("ImageJPEGTop", "Image")
        my_parser.register("GoalPerceptTop", "GoalPercept")
        my_parser.register("FieldPerceptTop", "FieldPercept")
        my_parser.register("BallCandidatesTop", "BallCandidates")

        frame_counter = 0
        print("log_path: ", log_path)
        game_log = LogReader(str(log_path), my_parser)
        
        for frame in tqdm(game_log):
            try:
                frame_number = frame['FrameInfo'].frameNumber
                frame_counter = frame_counter + 1
            except Exception as e:
                print(f"FrameInfo not found in current frame - {e}")
                continue

        print("\tframe_counter", frame_counter)
        try:

            response = client.logs.update(id=log_id, num_cognition_frames=frame_counter)
            print(f"\t{response}")
        except Exception as e:
            print(f"\terror inputing the data {log_path}")
            print(e)

        # parse the sensor log
        print()
        print("parse the sensor log")
        frame_counter = 0
        print("log_path: ", log_path)
        game_log = LogReader(str(sensor_log_path), my_parser)

        for frame in tqdm(game_log):
            try:
                frame_number = frame['FrameInfo'].frameNumber
                frame_counter = frame_counter + 1
            except Exception as e:
                print(f"FrameInfo not found in current frame - {e}")
                continue

        print("\tframe_counter", frame_counter)
        try:
            response = client.logs.update(id=log_id, num_motion_frames=frame_counter)
            print(f"\t{response}")
        except Exception as e:
            print(f"\terror inputing the data {log_path}")
            print(e)

