from ..vaapi.vaapi import vaapi
from requests.auth import HTTPBasicAuth
baseurl = "http://127.0.0.1:8000/api/"
username = "uwer"
password = "tester1"

Hauth = HTTPBasicAuth(username,password)


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
    test = vaapi(baseurl,Hauth)
    
    #print(test.get_log())
    #test.add_camera_matrix(CameraMatrix)
    print(test.get_log())
    print(test.add_image(Image))
    print(test.get_image())
    test.add_imageannotation(ImageAnnotation)

    

