import requests,logging

class client:
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
            response = self.session.post(f"{self.base_url}{endpoint}/",data=data, auth=self.auth)
            response.raise_for_status()  
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.debug(f"Error making Request:\n{e}")
            return
        
    def patch(self,endpoint:str,data:dict,parameter=None):
        #not sure explicit or implicit would be better
        endpoint = f"{endpoint}/{parameter}/"
        #endpoint = f"{endpoint}/{data.get("id")}/"
        try:
            response = self.session.patch(self.base_url+endpoint,data=data, auth=self.auth)
            response.raise_for_status()  
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.debug(f"Error making Request:\n{e}")
            return
    #event 
    def get_event(self,id=None): 
        return self.get("events",id)    
    
    def add_event(self,event:dict):
        return self.post("events",event)
    
    def change_event(self,event:dict,id=None):
        return self.patch("events",event,id)
    
    #games
    def get_games(self,id=None): 
        return self.get("games",id)    
    
    def add_games(self,games:dict):
        return self.post("games",games)
    
    def change_games(self,games:dict,id=None):
        return self.patch("games",games,id)
    
    #logs
    def get_log(self,id=None): 
        return self.get("logs",id)    
    
    def add_log(self,log:dict):
        return self.post("logs",log)
    
    def change_log(self,log:dict,id=None):
        return self.patch("logs",log,id)
    

    #CameraMatrix
    def get_camera_matrix(self,id=None): 
        return self.get("camera_matrix",id)    
    
    def add_camera_matrix(self,camera_matrix:dict):
        return self.post("camera_matrix",camera_matrix)
    
    def change_camera_matrix(self,camera_matrix:dict,id=None):
        return self.patch("camera_matrix",camera_matrix,id)
    
    #Image
    def get_image(self,id=None): 
        return self.get("image",id)    
    
    def add_image(self,image:dict):
        return self.post("image",image)
    
    def change_image(self,image:dict,id=None):
        return self.patch("image",image,id)
    
    #Image Annotation
    def get_imageannotation(self,id=None): 
        return self.get("imageannotation",id)    
    
    def add_imageannotation(self,annotation:dict):
        return self.post("imageannotation",annotation)
    
    def change_imageannotation(self,annotation:dict,id=None):
        return self.patch("imageannotation",annotation,id)
    
