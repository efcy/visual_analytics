from pathlib import Path
from naoth.log import Reader as LogReader
from naoth.log import Parser
import os
from google.protobuf.json_format import MessageToDict
from vaapi.client import Vaapi
from tqdm import tqdm
import argparse

def is_done(data, status_dict):
    # TODO get log_status representation here and check each field.
    try:
        response = client.log_status.list(log_id=data.id)
        if len(response) == 0:
            return False
        log_status = response[0]

        for k,v in status_dict.items():
            if k == "FrameInfo":
                k = "num_cognition_frames"
            field_value = getattr(log_status, k)
            
            if field_value == None:
                print(f"\tdid not find a value for repr {k}")
                return False
            client.log_status.list(log_id=data.id)
        return True
    # TODO would be nice to handle the vaapi Apierror here explicitely
    except Exception as e:
        print("error", e)
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force", action="store_true", default=False)
    args = parser.parse_args()

    log_root_path = os.environ.get("VAT_LOG_ROOT")
    log_root_path = "/mnt/c/RoboCup/rc24"
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    existing_data = client.logs.list()

    def sort_key_fn(data):
        return data.log_path

    for data in sorted(existing_data, key=sort_key_fn, reverse=True):
        log_id = data.id
        log_path = Path(log_root_path) / data.log_path
        sensor_log_path = Path(log_root_path) / data.sensor_log_path

        print("log_path: ", log_path)

        status_dict = {
            'BallModel': 0,
            'CameraMatrix': 0,
            'CameraMatrixTop': 0,
            'FieldPercept': 0,
            'FieldPerceptTop': 0,
            'GoalPercept': 0,
            'GoalPerceptTop': 0,
            'RansacLinePercept': 0,
            'RansacCirclePercept2018':0,
            'ShortLinePercept': 0,
            'ScanLineEdgelPercept': 0,
            'ScanLineEdgelPerceptTop': 0,
            "FrameInfo": 0,
        }

        if is_done(data, status_dict) and not args.force:
            print("\twe already calculated number of full frames for this log")
        else:
            my_parser = Parser()
            my_parser.register("FieldPerceptTop", "FieldPercept")
            my_parser.register("GoalPerceptTop", "GoalPercept")
            my_parser.register("FieldPerceptTop", "FieldPercept")
            my_parser.register("BallCandidatesTop", "BallCandidates")
            frame_counter = 0
            game_log = LogReader(str(log_path), my_parser)
            for idx, frame in enumerate(tqdm(game_log)):
                # stop parsing log if FrameInfo is missing
                try:
                    frame_number = frame['FrameInfo'].frameNumber
                except Exception as e:
                    print(f"FrameInfo not found in current frame - will not parse any other frames from this log and continue with the next one")
                    continue

                for repr in status_dict:
                    try:
                        data = MessageToDict(frame[repr])
                        status_dict[repr] += 1
                    except AttributeError:
                        # TODO only print something when in debug mode
                        #print("skip frame because representation is not present")
                        continue
                    except Exception as e:
                        print(f"error parsing {repr} in log {log_path} at frame {idx}")
                        print({e})

            try:
                response = client.log_status.create(
                log_id=log_id, 
                BallModel=status_dict['BallModel'],
                CameraMatrix=status_dict['CameraMatrix'],
                CameraMatrixTop=status_dict['CameraMatrixTop'],
                FieldPercept=status_dict['FieldPercept'],
                FieldPerceptTop=status_dict['FieldPerceptTop'],
                GoalPercept=status_dict['GoalPercept'],
                GoalPerceptTop=status_dict['GoalPerceptTop'],
                RansacLinePercept=status_dict['RansacLinePercept'],
                ShortLinePercept=status_dict['ShortLinePercept'],
                ScanLineEdgelPercept=status_dict['ScanLineEdgelPercept'],
                ScanLineEdgelPerceptTop=status_dict['ScanLineEdgelPerceptTop'],
                RansacCirclePercept2018=status_dict['RansacCirclePercept2018'],
                num_cognition_frames=status_dict['RansacCirclePercept2018']
                )
                print(f"\t{response}")
            except Exception as e:
                print(f"\terror inputing the data {log_path}")
                print(e)

        continue

        # TODO figure out how we should handle adding additional representations?
        # NOTE when we use create above we have to use update for sensor log,
        """
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
        """