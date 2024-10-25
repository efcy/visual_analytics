"""
    test for a maybe a more space efficient implementation
"""
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
    num_cognition_frames =log_status.num_cognition_frames
    if not num_cognition_frames or int(num_cognition_frames) == 0:
        print("\tWARNING: first calculate the number of cognitions frames and put it in the db")
        quit()

    # query the cognition representation and check how many frames with a given representations are there
    new_list = list()
    for repr in representation_list:
        num_repr_frames= len(client.cognition_repr.list(log_id=log_id, representation_name=repr))
        print(f"\t{repr} inserted frames: {num_repr_frames}/{getattr(log_status, repr)}")
        if getattr(log_status, repr) != num_repr_frames:
            new_list.append(repr)
    return new_list
        

if __name__ == "__main__":
    log_root_path = os.environ.get("VAT_LOG_ROOT")
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    existing_data = client.logs.list()

    def sort_key_fn(data):
        return data.log_path

    for data in sorted(existing_data, key=sort_key_fn, reverse=True):
        log_id = data.id

        #if int(data.game_id) != 57 and int(data.game_id) != 58:
        #    print(int(data.game_id))
        #    continue

        log_path = Path(log_root_path) / data.log_path
        print("log_path: ", log_path)

        representation_list = ["BallModel","CameraMatrix", "CameraMatrixTop", "FieldPercept", "FieldPerceptTop", "GoalPercept", "GoalPerceptTop", "RansacLinePercept", "ShortLinePercept", "ScanLineEdgelPercept", "ScanLineEdgelPerceptTop", "RansacCirclePercept2018"]
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

        game_log = LogReader(str(log_path), my_parser)

        my_array = list()
        for idx, frame in enumerate(tqdm(game_log, desc=f"Parsing frame", leave=True)):
            json_frame_obj = {
                "log_id":log_id, 
                "frame_number":frame_number,
                "representation_data":data
            }
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

                json_repr_obj = {
                    "representation_name":data,
                }
                json_frame_obj.update({json_repr_obj})
            my_array.append(json_frame_obj)
            if idx % 200 == 0:
                try:
                    response = client.cognition_repr.bulk_create(
                        repr_list=my_array
                    )
                    my_array.clear()
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
