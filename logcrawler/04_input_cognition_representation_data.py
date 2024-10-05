from pathlib import Path
from naoth.log import Reader as LogReader
from naoth.log import Parser
from google.protobuf.json_format import MessageToDict
import os
from tqdm import tqdm
from vaapi.client import Vaapi

def is_input_done(representation_list):
    # query the cognition representation first and check how many frames with a given representations are there
    # FIXME this fails when we have representations that are not written in every frame
    new_list = list()
    for repr in representation_list:
        num_repr_frames= len(client.cognition_repr.list(log_id=log_id, representation_name=repr))
        if num_cognition_frames != num_repr_frames:
            new_list.append(repr)
    return new_list
        

if __name__ == "__main__":
    log_root_path = os.environ.get("VAT_LOG_ROOT")
    #log_root_path = "/mnt/c/RoboCup/rc24"
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    existing_data = client.logs.list()

    def sort_key_fn(data):
        return data.log_path

    for data in sorted(existing_data, key=sort_key_fn, reverse=True):
        log_id = data.id

        if int(data.game_id) != 17 and int(data.game_id) != 12:
            print(int(data.game_id))
            continue


        log_path = Path(log_root_path) / data.log_path
        print("log_path: ", log_path)

        # check if number of frames were calculated already
        num_cognition_frames = data.num_cognition_frames
        if not num_cognition_frames or int(num_cognition_frames) == 0:
            print("\tWARNING: first calculate the number of cognitions frames and put it in the db")
            continue
        
        #, "RansacLinePercept""ShortLinePercept",
        representation_list = ["RansacLinePercept", "ShortLinePercept", "ScanLineEdgelPercept", "ScanLineEdgelPerceptTop"]
        # check if we need to insert this log
        representation_list = is_input_done(representation_list)
        if len(representation_list) == 0:
            print("\tall required representations are already inserted, will continue with the next log")
            continue
        
        my_parser = Parser()
        my_parser.register("ImageJPEG"   , "Image")
        my_parser.register("ImageJPEGTop", "Image")
        my_parser.register("GoalPerceptTop", "GoalPercept")
        my_parser.register("FieldPerceptTop", "FieldPercept")
        my_parser.register("BallCandidatesTop", "BallCandidates")
        
        batch_size = 200
        counter = 0
        

        game_log = LogReader(str(log_path), my_parser)

        my_array = list()
        for idx, frame in enumerate(tqdm(game_log, desc=f"Parsing frame", leave=True)):
            for repr_name in frame.get_names():
                if not repr_name in representation_list:
                    continue
                
                # try accessing framenumber directly because we can have the situation where the framenumber is missing in the
                # last frame
                try:
                    frame_number = frame['FrameInfo'].frameNumber
                except Exception as e:
                    print(f"FrameInfo not found in current frame - will not parse any other representation from this frame")
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
                    "frame_number":frame_number,
                    "representation_name":repr_name,
                    "representation_data":data
                }
                my_array.append(json_obj)

            if idx % 10 == 0:
                try:
                    response = client.cognition_repr.bulk_create(
                        repr_list=my_array
                    )
                    counter=0
                except Exception as e:
                    print(e)
                    print(f"error inputing the data {log_path}")
                    quit()
        # handle the last frames
        # just upload whatever is in the array. There will be old data but that does not matter, it will be filtered out on insertion
        try:
            response = client.cognition_repr.bulk_create(
                repr_list=my_array
            )
            print(response)
        except Exception as e:
            print(e)
            print(f"error inputing the data {log_path}")
