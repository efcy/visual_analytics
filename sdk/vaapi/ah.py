from sdk.vaapi.old import client
import logging

baseurl = "http://127.0.0.1:8000/api/"
#key can be created on admin site
key = "Ajfnatkg.pDyZAUl0eMS5zIym8amPpy4X7yRKJlXX"


#set to DEBUG to see more detailed logging messages
logging.basicConfig(level=logging.ERROR)

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
    #using the health checkpoint without authentication
    test = client(baseurl,"wrong-key")
    print(test.check_connection())
    #everything else only works while authenticated
    test1 = client(baseurl,key)
    #lists only events with name test
    print(test1.list_events({"name":"test"}))
    print(test1.add_event(event))

    #print(test.get_log())
    #test.add_camera_matrix(CameraMatrix)
   

    

