from .vaapi import vaapi
from requests.auth import HTTPBasicAuth
baseurl = "http://localhost:8000/api/"
username = "uwer"
password = "tester1"

Hauth = HTTPBasicAuth(username,password)




if __name__ == "__main__":
    test =   vaapi(baseurl,Hauth)
    print(test.get_event())
    print(test.get_event(4))

