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
        return data.log_path

    for data in sorted(existing_data, key=sort_key_fn):
        log_id = data.id
        num_cognition_frames = data.num_cognition_frames
        
        # check if number of frames were calculated already
        if not num_cognition_frames or int(num_cognition_frames) == 0:
            print("\tWARNING: first calculate the number of cognitions frames and put it in the db")
            continue

        # query the cognition representation first and check how many frameinfo representations are there
        num_frame_info_db = len(client.cognition_repr.list(log_id=log_id, representation_name="FrameInfo"))
        if num_cognition_frames == num_frame_info_db:
            print("\tall frameinfo representations are already written to the database - continue with next log")
            continue

        log_path = Path(log_root_path) / data.log_path

        my_parser = Parser()
        my_parser.register("ImageJPEG"   , "Image")
        my_parser.register("ImageJPEGTop", "Image")
        my_parser.register("GoalPerceptTop", "GoalPercept")
        my_parser.register("FieldPerceptTop", "FieldPercept")
        my_parser.register("BallCandidatesTop", "BallCandidates")
        
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
                
                # try accessing framenumber directly because we can have the situation where the framenumber is missing in the
                # last frame
                try:
                    frame_number = frame['FrameInfo'].frameNumber
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
                    "frame_number":frame_number,
                    "representation_name":repr_name,
                    "representation_data":data
                }
                my_array[counter] = json_obj
                counter = counter + 1
                if counter == batch_size:
                    try:
                        response = client.cognition_repr.bulk_create(
                            repr_list=my_array
                        )
                        print(frame_number)
                        print(f"\t{response}")
                        counter=0
                    except Exception as e:
                        print(f"error inputing the data {log_path}")
        # handle the last frames
        # just upload whatever is in the array. There will be old data but that does not matter, it will be filtered out on insertion
        try:
            response = client.cognition_repr.bulk_create(
                repr_list=my_array
            )
            print(response)
        except Exception as e:
            print(f"error inputing the data {log_path}")
        # only do the first log for now
        break
