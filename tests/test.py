from naoth.log import Reader as LogReader
from vaapi import client
import json
baseurl = "http://127.0.0.1:8000/api/"
#key can be created on admin site
api_token = "514cf2e88eab425cfdfce652994d30a1a0c3b1ad"

if __name__ == "__main__":
    my_client = client(baseurl,api_token)
    existing_events = my_client.list_events()
    print(existing_events)
    for e in existing_events:
        print(e["name"])