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

    def myfunc(data):
        return data.log_path

    for data in sorted(existing_data, key=myfunc):
        log_id = data.id
        log_path = Path(log_root_path) / data.log_path

        my_parser = Parser()
        my_parser.register("ImageJPEG"   , "Image")
        my_parser.register("ImageJPEGTop", "Image")
        my_parser.register("GoalPerceptTop", "GoalPercept")
        my_parser.register("FieldPerceptTop", "FieldPercept")
        my_parser.register("BallCandidatesTop", "BallCandidates")
        
        batch_size = 100
        counter = 0
        print("log_path: ", log_path)
        game_log = LogReader(str(log_path), my_parser)
        try:
            my_array = [None] * batch_size
            for frame in game_log:
                #print(f"\t{frame.get_names()}")
                print(frame['FrameInfo'].frameNumber)
                for repr_name in frame.get_names():
                    if repr_name == "FrameInfo":
                        continue
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

                    data = MessageToDict(frame[repr_name])
                    json_obj = {
                        "log_id":log_id, 
                        "frame_number":frame['FrameInfo'].frameNumber,
                        "representation_name":repr_name,
                        "representation_data":data
                    }
                    my_array[counter] = json_obj
                    counter = counter + 1
                    if counter == batch_size:                        
                        response = client.cognition_repr.bulk_create(
                            repr_list=my_array
                        )
                        print(response)
                        counter=0
                    
        except Exception as e:
            print(repr_name)
            print(f"error parsing the log or inserting it: {e}")
        break
