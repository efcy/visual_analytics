from pathlib import Path
from naoth.log import Reader as LogReader
from naoth.log import Parser
import os
from vaapi.client import Vaapi
from tqdm import tqdm
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force", action="store_true", default=False)
    args = parser.parse_args()

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
        updated_log_path = log_path.parent / "game.log"

        print("log_path: ", log_path)

        if data.num_cognition_frames and int(data.num_cognition_frames) > 0 and not args.force:
            print("\twe already calculated number of full frames for this log")
        else:
            my_parser = Parser()
            my_parser.register("FieldPerceptTop", "FieldPercept")
            frame_counter = 0
            game_log = LogReader(str(updated_log_path), my_parser)
            for frame in tqdm(game_log):
                try:
                    # actually we need to check for all cognition representations here that we care about otherwise we get in trouble when 
                    # checking a representation later that is not in the last frame but frameInfo is. There will always be a mismatch

                    # we cant use the list of representations here because some of the representations like AudioData are not written in every frame
                    frame_number = frame['FrameInfo'].frameNumber
                    BallModel = frame['BallModel']
                    BehaviorStateSparse = frame['BehaviorStateSparse']
                    CameraMatrixTop = frame['CameraMatrixTop']
                    CameraMatrix = frame['CameraMatrix']
                    OdometryData = frame['OdometryData']
                    FieldPercept = frame['FieldPercept']
                    FieldPerceptTop = frame['FieldPerceptTop']

                except Exception as e:
                    print(f"FrameInfo not found in current frame - {e}")
                    continue

                frame_counter = frame_counter + 1
            print("\tframe_counter", frame_counter)
            try:
                response = client.logs.update(id=log_id, num_cognition_frames=frame_counter)
                print(f"\t{response}")
            except Exception as e:
                print(f"\terror inputing the data {updated_log_path}")
                print(e)

        # parse the sensor log
        if data.num_motion_frames and int(data.num_motion_frames) > 0 and not args.force:
            print("\twe already calculated number of motion frames for this log")
        else:
            print()
            print("parse the sensor log")
            frame_counter = 0
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
