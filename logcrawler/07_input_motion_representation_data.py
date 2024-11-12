from pathlib import Path
from naoth.log import Reader as LogReader
from naoth.log import Parser
from google.protobuf.json_format import MessageToDict
import os
from tqdm import tqdm
from vaapi.client import Vaapi


def is_input_done(representation_list):
    # get the log status - showing how many entries per representation there should be
    try:
        # we use list here because we only know the log_id here and not the if of the logstatus object
        response = client.log_status.list(log_id=data.id)
        if len(response) == 0:
            return False
        log_status = response[0]
    except Exception as e:
        print(e)

    # check if number of frames were calculated already
    num_motion_frames = log_status.num_motion_frames
    if not num_motion_frames or int(num_motion_frames) == 0:
        print("\tWARNING: first calculate the number of motion frames and put it in the db")
        quit()

    # query the cognition representation and check how many frames with a given representations are there
    response = client.motion_repr.get_repr_count(log_id=log_id)

    new_list = list()
    for repr in representation_list:
        # if no entry for a given representation is present this will throw an error
        try:
            if repr == "FrameInfo":
                # handle this differently because we called the field num_motion_frames in the db
                # FIXME fix the db schema so that this code can be easier
                num_repr_frames=response[repr]
                print(f"\t{repr} inserted frames: {num_repr_frames}/{getattr(log_status, 'num_motion_frames')}")
                if int(getattr(log_status, "num_motion_frames")) != int(num_repr_frames):
                    new_list.append(repr)
            else:
                num_repr_frames=response[repr]
                print(f"\t{repr} inserted frames: {num_repr_frames}/{getattr(log_status, repr)}")
                if int(getattr(log_status, repr)) != int(num_repr_frames):
                    new_list.append(repr)
        except:
            new_list.append(repr)
        
    if len(new_list) > 0:
        print("\tneed to run insertion again")
        print(f"{new_list}")
    return new_list


if __name__ == "__main__":
    log_root_path = os.environ.get("VAT_LOG_ROOT")
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    existing_data = client.logs.list()

    def sort_key_fn(data):
        return data.sensor_log_path

    for data in sorted(existing_data, key=sort_key_fn, reverse=True):
        log_id = data.id

        log_path = Path(log_root_path) / data.sensor_log_path
        print("log_path: ", log_path)

        representation_list = [
            "FrameInfo",
            "IMUData", 
            "FSRData", 
            "ButtonData", 
            "SensorJointData", 
            "AccelerometerData", 
            "InertialSensorData", 
            "MotionStatus",
            "MotorJointData",
            "GyrometerData",
        ]
        # check if we need to insert this log
        representation_list = is_input_done(representation_list)
        if len(representation_list) == 0:
            print("\tall required representations are already inserted, will continue with the next log")
            continue

        my_parser = Parser()
        game_log = LogReader(str(log_path), my_parser)
        
        my_array = list()
        for idx, frame in enumerate(tqdm(game_log, desc=f"Parsing frame", leave=True)):
            for repr_name in frame.get_names():
                if not repr_name in representation_list:
                    continue
                
                # try accessing framenumber directly because we can have the situation where the framenumber is missing in the
                # last frame
                try:
                    sensor_frame_number = frame['FrameInfo'].frameNumber
                    sensor_frame_time = frame['FrameInfo'].time
                except Exception as e:
                    print(f"FrameInfo not found in current frame - will not parse any other representation from this frame")
                    print({e})
                    break

                try:
                    data = MessageToDict(frame[repr_name])
                except AttributeError:
                    #print("skip frame because representation is not present")
                    continue               
                except Exception as e:
                    print(repr_name)
                    print(f"error parsing the log {log_path}")
                    print({e})
                    quit()

                json_obj = {
                    "log_id":log_id, 
                    "sensor_frame_number":sensor_frame_number,
                    "sensor_frame_time": sensor_frame_time,
                    "representation_name":repr_name,
                    "representation_data":data
                }
                my_array.append(json_obj)

            if idx % 100 == 0:
                try:
                    response = client.motion_repr.bulk_create(
                        repr_list=my_array
                    )
                    my_array.clear()
                except Exception as e:
                    print(f"error inputing the data {log_path}")
                    print(e)
                    quit()
        # handle the last frames
        # just upload whatever is in the array. There will be old data but that does not matter, it will be filtered out on insertion
        try:
            response = client.motion_repr.bulk_create(
                repr_list=my_array
            )
            print(response)
        except Exception as e:
            print(f"error inputing the data {log_path}")
        # only do the first log for now
