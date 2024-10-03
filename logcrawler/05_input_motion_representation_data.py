from pathlib import Path
from naoth.log import Reader as LogReader
from naoth.log import Parser
from google.protobuf.json_format import MessageToDict
import os
from tqdm import tqdm
from vaapi.client import Vaapi


if __name__ == "__main__":
    log_root_path = os.environ.get("VAT_LOG_ROOT")
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    existing_data = client.logs.list()

    def sort_key_fn(data):
        return data.sensor_log_path

    for data in sorted(existing_data, key=sort_key_fn):
        log_id = data.id
        num_motion_frames = data.num_motion_frames
        
        # check if number of frames were calculated already
        if not num_motion_frames or num_motion_frames == 0:
            print("\tWARNING: first calculate the number of motion frames and put it in the db")
            continue

        # query the motion representation first and check how many frameinfo representations are there
        num_frame_info_db = len(client.motion_repr.list(log_id=log_id, representation_name="FrameInfo"))
        if num_motion_frames == num_frame_info_db:
            print("\tall frameinfo representations are already written to the database - continue with next log")
            continue

        log_path = Path(log_root_path) / data.sensor_log_path

        my_parser = Parser()

        
        batch_size = 200
        counter = 0
        print("log_path: ", log_path)
        game_log = LogReader(str(log_path), my_parser)
        
        my_array = [None] * batch_size
        for frame in game_log:
            for repr_name in frame.get_names():
                if frame[repr_name] == None:
                    # ScanLineEdgelPercept is empty but we write it anyway to the log
                    continue
                
                # try accessing framenumber directly because we can have the situation where the framenumber is missing in the
                # last frame
                try:
                    sensor_frame_number = frame['FrameInfo'].frameNumber
                except Exception as e:
                    print(f"FrameInfo not found in current frame - will not parse any other representation from this frame")
                    print({e})
                    break

                try:
                    data = MessageToDict(frame[repr_name])                       
                except Exception as e:
                    print(repr_name)
                    print(f"error parsing the log {log_path}")
                    print({e})

                json_obj = {
                    "log_id":log_id, 
                    "sensor_frame_number":sensor_frame_number,
                    "representation_name":repr_name,
                    "representation_data":data
                }
                my_array[counter] = json_obj
                counter = counter + 1
                if counter == batch_size:
                    try:
                        response = client.motion_repr.bulk_create(
                            repr_list=my_array
                        )
                        print(sensor_frame_number)
                        print(f"\t{response}")
                        counter=0
                    except Exception as e:
                        print(f"error inputing the data {log_path}")
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
        break
