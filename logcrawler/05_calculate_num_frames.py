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
    try:
        # we use list here because we only know the log_id here and not the if of the logstatus object
        response = client.log_status.list(log_id=log_id)
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
        return True
    # TODO would be nice to handle the vaapi Apierror here explicitely
    except Exception as e:
        print("error", e)
        quit()
        return False


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

        if is_done(log_id, cognition_status_dict) and not args.force:
            print("\twe already calculated number of full cognition frames for this log")
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

                for repr in cognition_status_dict:
                    try:
                        data = MessageToDict(frame[repr])
                        cognition_status_dict[repr] += 1
                    except AttributeError:
                        # TODO only print something when in debug mode
                        #print("skip frame because representation is not present")
                        continue
                    except Exception as e:
                        print(f"error parsing {repr} in log {log_path} at frame {idx}")
                        print({e})

            try:
                response = client.log_status.update(
                log_id=log_id, 
                BallModel=cognition_status_dict['BallModel'],
                CameraMatrix=cognition_status_dict['CameraMatrix'],
                CameraMatrixTop=cognition_status_dict['CameraMatrixTop'],
                FieldPercept=cognition_status_dict['FieldPercept'],
                FieldPerceptTop=cognition_status_dict['FieldPerceptTop'],
                GoalPercept=cognition_status_dict['GoalPercept'],
                GoalPerceptTop=cognition_status_dict['GoalPerceptTop'],
                RansacLinePercept=cognition_status_dict['RansacLinePercept'],
                ShortLinePercept=cognition_status_dict['ShortLinePercept'],
                ScanLineEdgelPercept=cognition_status_dict['ScanLineEdgelPercept'],
                ScanLineEdgelPerceptTop=cognition_status_dict['ScanLineEdgelPerceptTop'],
                RansacCirclePercept2018=cognition_status_dict['RansacCirclePercept2018'],
                OdometryData=cognition_status_dict['OdometryData'],
                num_cognition_frames=cognition_status_dict['FrameInfo']
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
        if is_done(log_id, motion_status_dict) and not args.force:
            print("\twe already calculated number of full sensor frames for this log")
        else:
            my_parser = Parser()
            game_log = LogReader(str(sensor_log_path), my_parser)
            for idx, frame in enumerate(tqdm(game_log)):
                # stop parsing log if FrameInfo is missing
                try:
                    frame_number = frame['FrameInfo'].frameNumber
                except Exception as e:
                    print(f"FrameInfo not found in current frame - will not parse any other frames from this log and continue with the next one")
                    continue
                for repr in motion_status_dict:
                    try:
                        data = MessageToDict(frame[repr])
                        motion_status_dict[repr] += 1
                    except AttributeError:
                        # TODO only print something when in debug mode
                        #print("skip frame because representation is not present")
                        continue
                    except Exception as e:
                        print(f"error parsing {repr} in log {log_path} at frame {idx}")
                        print({e})

            try:
                response = client.log_status.update(
                log_id=log_id, 
                IMUData=motion_status_dict['IMUData'],
                FSRData=motion_status_dict['FSRData'],
                ButtonData=motion_status_dict['ButtonData'],
                SensorJointData=motion_status_dict['SensorJointData'],
                AccelerometerData=motion_status_dict['AccelerometerData'],
                InertialSensorData=motion_status_dict['InertialSensorData'],
                MotionStatus=motion_status_dict['MotionStatus'],
                MotorJointData=motion_status_dict['MotorJointData'],
                GyrometerData=motion_status_dict['GyrometerData'],
                num_motion_frames=motion_status_dict['FrameInfo']
                )
            except Exception as e:
                print(f"\terror inputing the data {log_path}")
                print(e)
