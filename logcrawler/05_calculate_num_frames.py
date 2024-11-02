from pathlib import Path
from naoth.log import Reader as LogReader
from naoth.log import Parser
import os
from google.protobuf.json_format import MessageToDict
from vaapi.client import Vaapi
from tqdm import tqdm
import argparse

def is_done(log_id, status_dict):
    # TODO get log_status representation here and check each field.
    new_dict = status_dict.copy()
    try:
        # we use list here because we only know the log_id here and not the if of the logstatus object
        response = client.log_status.list(log_id=log_id)
        if len(response) == 0:
            return status_dict
        log_status = response[0]

        for k,v in status_dict.items():
            if k == "FrameInfo":
                field_value = getattr(log_status, "num_cognition_frames")
            else:
                field_value = getattr(log_status, k)
            
            if field_value == None:
                print(f"\tdid not find a value for repr {k}")
            else:
                new_dict.pop(k)
        return new_dict
    # TODO would be nice to handle the vaapi API error here explicitely
    except Exception as e:
        print("error", e)
        quit()
        return status_dict


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

    def sort_key_fn(data):
        return data.log_path

    for log_data in sorted(existing_data, key=sort_key_fn, reverse=True):
        log_id = log_data.id
        log_path = Path(log_root_path) / log_data.log_path
        sensor_log_path = Path(log_root_path) / log_data.sensor_log_path

        print("log_path: ", log_path)

        cognition_status_dict = {
            'BallModel': 0,
            'BallCandidates': 0,
            'BallCandidatesTop': 0,
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
            'OdometryData': 0,
            "FrameInfo": 0,
        }

        new_cognition_status_dict = is_done(log_id, cognition_status_dict)
        if not args.force and len(new_cognition_status_dict) == 0:
            print("\twe already calculated number of full cognition frames for this log")
        else:
            if args.force:
                new_cognition_status_dict = cognition_status_dict
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
                # TODO: speed it up by removing representations that we dont care about in this dict
                for repr in new_cognition_status_dict:
                    try:
                        data = MessageToDict(frame[repr])
                        new_cognition_status_dict[repr] += 1
                    except AttributeError:
                        # TODO only print something when in debug mode
                        #print("skip frame because representation is not present")
                        continue
                    except Exception as e:
                        print(f"error parsing {repr} in log {log_path} at frame {idx}")
                        print({e})

            try:
                # rename the dict key such that it matches what the database expects here
                new_cognition_status_dict['num_cognition_frames'] = new_cognition_status_dict.pop('FrameInfo')
                
                response = client.log_status.update(
                log_id=log_id, 
                **new_cognition_status_dict
                )
            except Exception as e:
                print(f"\terror inputing the data {log_path}")
                print(e)
            

        # TODO figure out how we should handle adding additional representations?
        # NOTE when we use create above we have to use update for sensor log,
        motion_status_dict = {
            'FrameInfo': 0,
            'IMUData': 0,
            'FSRData': 0,
            'ButtonData': 0,
            'SensorJointData': 0,
            'AccelerometerData': 0,
            'InertialSensorData': 0,
            'MotionStatus': 0,
            'MotorJointData':0,
            'GyrometerData': 0,
        }

        new_motion_status_dict = is_done(log_id, motion_status_dict)
        if not args.force and len(new_motion_status_dict) == 0:
            print("\twe already calculated number of full sensor frames for this log")
        else:
            if args.force:
                new_motion_status_dict = motion_status_dict
            my_parser = Parser()
            game_log = LogReader(str(sensor_log_path), my_parser)
            for idx, frame in enumerate(tqdm(game_log)):
                # stop parsing log if FrameInfo is missing
                try:
                    frame_number = frame['FrameInfo'].frameNumber
                except Exception as e:
                    print(f"FrameInfo not found in current frame - will not parse any other frames from this log and continue with the next one")
                    continue
                for repr in new_motion_status_dict:
                    try:
                        data = MessageToDict(frame[repr])
                        new_motion_status_dict[repr] += 1
                    except AttributeError:
                        # TODO only print something when in debug mode
                        #print("skip frame because representation is not present")
                        continue
                    except Exception as e:
                        print(f"error parsing {repr} in log {log_path} at frame {idx}")
                        print({e})

            try:
                new_motion_status_dict['num_motion_frames'] = new_motion_status_dict.pop('FrameInfo')
                response = client.log_status.update(
                log_id=log_id, 
                **new_motion_status_dict
                )
            except Exception as e:
                print(f"\terror inputing the data {log_path}")
                print(e)
