import requests,logging



class vaapi:
    def __init__(self,base_url:str,auth):
        self.base_url = base_url
        self.auth = auth
        #we are creating a session to reduce time and resources for each request
        self.session = requests.Session()
        self.headers = {"Connection": "keep-alive" ,"Content-Type": "application/json"}
    def get(self,endpoint,parameter):
        endpoint = f"{endpoint}/{parameter}" if parameter is not None else f"{endpoint}/" 
        try:
            logging.debug(self.base_url+endpoint)
            response =self.session.get(self.base_url+endpoint, auth=self.auth)
            response.raise_for_status()  
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.debug(f"Error making Request:\n{e}")
            return
        
    def post(self,endpoint:str,data:dict):
        try:
            response = self.session.post(self.base_url+endpoint,data=data, auth=self.auth)
            response.raise_for_status()  
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.debug(f"Error making Request:\n{e}")
            return
        
    def patch(self,endpoint:str,data:dict,parameter=None):
        #not sure explicit or implicit would be better
        #endpoint = f"{endpoint}/{parameter}/"
        endpoint = f"{endpoint}/{data.get("id")}/"
        try:
            response = self.session.patch(self.base_url+endpoint,data=data, auth=self.auth)
            response.raise_for_status()  
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.debug(f"Error making Request:\n{e}")
            return

    def get_event(self,id=None): 
        return self.get("events",id)    
    
    def add_event(self,event:dict):
        return self.post("events/",event)
    
    def change_event(self,event:dict,id=None):
        return self.patch("events",event,id)


                          