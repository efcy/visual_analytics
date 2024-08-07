from naoth.log import Reader as LogReader
from vaapi import client
import json
baseurl = "http://127.0.0.1:8000/api/"
#key can be created on admin site
api_token = "514cf2e88eab425cfdfce652994d30a1a0c3b1ad"

if __name__ == "__main__":
    my_client = client(baseurl,api_token)
    with LogReader("sensor.log") as reader:
        for frame in reader.read():
            #print(frame.get_names())
            print(frame['FrameInfo'])

            my_client.add_sensorlog_data({
                "sensor_frame_number": 1,
                "sensor_frame_time": 1,
                "representation_name": "IMUData",
                "representation_data": json.dumps(dict())
            })
            break