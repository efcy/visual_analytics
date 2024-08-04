#pip uninstall vaapi
#cd sdk
#python3 setup.py install
from vaapi import client
import logging,random

baseurl = "http://127.0.0.1:8000/api/"
#key can be created on admin site
api_token = "514cf2e88eab425cfdfce652994d30a1a0c3b1ad"


#set to DEBUG to see more detailed logging messages
logging.basicConfig(level=logging.ERROR)

def delete_all_frames(client : client):
    
    client.delete_all_frametimes()

def add_new_frames(client : client,count):
    frametime_list = []
    frame_number = 0
    frame_time = 0
    for _ in range(count):
        frametime_list.append({"frame_number":int(frame_number),"frame_time":int(frame_time)})
        frame_number+=1
        frame_time += random.randint(29,33) #simulating 30 to 34 fps

    client.add_frametime(frametime_list)

if __name__ == "__main__":
    test1 = client(baseurl,api_token)

    delete_all_frames(test1)
    add_new_frames(test1,2000)
    print(test1.list_frametimes())    
