import requests,logging

class vaapi:
    def __init__(self,base_url,auth):
        self.base_url = base_url
        self.auth = auth
        #we are creating a session to reduce time and resources for each request
        self.session = requests.Session()

    def get(self,endpoint):
        try:
            response =self.session.get(self.base_url+endpoint, auth=self.auth)
            response.raise_for_status()  
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.debug(f"Error making Request:\n{e}")
            return
        
    def post(self,endpoint,data):
        try:
            response = self.session.post(self.base_url+endpoint,data=data, auth=self.auth)
            response.raise_for_status()  
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.debug(f"Error making Request:\n{e}")
            return

    def get_event(self,id=""):
        return self.get("events/"+str(id))    
    
    def add_event(self,event):
        return self.post("events/",{"name":f"{event}"})
    
    