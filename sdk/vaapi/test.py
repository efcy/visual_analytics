from vaapi import client
import logging
from requests.auth import HTTPBasicAuth
baseurl = "http://127.0.0.1:8000/api/"
key = "WVerj5dm.Pvu8w2lzkyC2w2FqiIvepajEkSccAefP"

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#example objects
event = {"name":"Mexico"}
patch_event = {"id":10,"name":"México"}

game = {"event":10,"team1":"NaoTH","team2":"Brainstormers"}
patch_game = {"event":10,"team1":"Team Osaka","team2":"Brainstormers"}

log = {"game":8,"player_number":42}

CameraMatrix = {"log":2,"frame_number":1000}

Image = {"log":2,"type":"JPEG"}

ImageAnnotation = {"image":1,"type":"boundingbox"}

if __name__ == "__main__":
    test = client(baseurl,key)
    print(test.get_event())

    #print(test.get_log())
    #test.add_camera_matrix(CameraMatrix)
   

    

