from naoth.log import Reader as LogReader
from google.protobuf.json_format import MessageToDict
from pathlib import Path
from vaapi import client
import json
baseurl = "http://127.0.0.1:8000/api/"
#key can be created on admin site
api_token = "514cf2e88eab425cfdfce652994d30a1a0c3b1ad"

if __name__ == "__main__":
    # FIXME use environment variables for this
    root_path = "/mnt/q/"
    my_client = client(baseurl,api_token)
    existing_data = my_client.list_robot_data()

    for data in existing_data:
        robot_data_id = data["id"]
        print(data["sensor_log_path"])
        sensor_log_path = Path(root_path) / data["sensor_log_path"]
        with LogReader(sensor_log_path) as reader:
            for frame in reader.read():
                for name in frame.get_names():
                    if name == "FrameInfo":
                        continue
                    data = MessageToDict(frame[name])
                    my_client.add_sensorlog_data({
                        "robotdata": robot_data_id,
                        "sensor_frame_number": frame['FrameInfo'].frameNumber,
                        "sensor_frame_time": frame['FrameInfo'].time,
                        "representation_name": name,
                        "representation_data": json.dumps(data)
                    })
        break
    