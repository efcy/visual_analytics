import requests,logging

class client:
    def __init__(self,
                 url:str,
                 api_token:str
                 ):
        self.url = url
        
        self.headers = {"Authorization": f"Token  {api_token}",
                        "Connection": "keep-alive" ,
                        "Content-Type": "application/json"}
#
        self.session = requests.Session()

    def make_request(self, method, endpoint, *args, **kwargs):
        """
        Make an HTTP request to the specified endpoint.

        Args:
            method (str): The HTTP method (GET, POST, PATCH, DELETE).
            endpoint (str): The API endpoint.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: The JSON response from the API.

        Raises:
            requests.exceptions.RequestException: If the request fails.
        """
        try:
            url = f"{self.url}{endpoint}/"
            response = self.session.request(method, url, headers=self.headers, *args, **kwargs)
            response.raise_for_status()
            #delete requests don't json responses this is a quick hack to avoid errors
            if method == "DELETE":
                return response
            else:  
                return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error while making {method} request to {url}\n"
                        f"Headers: {self.headers}\n"
                        f"Args: {args}\n"
                        f"Kwargs: {kwargs}\n"
                        f"Error: {e}")

    def check_connection(self):
        """
        Call  /health endpoint to check the connection to the server.

        Returns
        -------
        dict
            Status string like "UP"
        """
        return self.make_request("GET","health")

    # Event
    def list_events(self, query_params=None):
        """
        List all events.

        Args:
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the list of events.
        """
        return self.make_request("GET", "events", params=query_params)

    def get_event(self, id, query_params=None):
        """
        Get a specific event.

        Args:
            id (int): The ID of the event.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the event details.
        """
        return self.make_request("GET", f"events/{id}", params=query_params)

    def add_event(self, event: dict, query_params=None):
        """
        Add a new event.

        Args:
            event (dict): The event data to be added.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the added event details.
        """
        # FIXME improve this code
        existing_events = self.list_events()
        for e in existing_events:
            if e["name"] == event["name"]:
                #print("WARNING: name already exists")
                return e
        return self.make_request("POST", "events", json=event, params=query_params)

    def change_event(self, id, event: dict, query_params=None):
        """
        Update an existing event.

        Args:
            id (int): The ID of the event to update.
            event (dict): The updated event data.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the updated event details.
        """
        return self.make_request("PATCH", f"events/{id}", json=event, params=query_params)

    def delete_event(self, id, query_params=None):
        """
        Delete an event.

        Args:
            id (int): The ID of the event to delete.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response confirming the deletion.
        """
        return self.make_request("DELETE", f"events/{id}", params=query_params)

    # Games
    def list_games(self, query_params=None):
        """
        List all games.

        Args:
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the list of games.
        """
        return self.make_request("GET", "games", params=query_params)

    def get_games(self, id, query_params=None):
        """
        Get a specific game.

        Args:
            id (int): The ID of the game.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the game details.
        """
        return self.make_request("GET", f"games/{id}", params=query_params)

    def add_games(self, games: dict, query_params=None):
        """
        Add a new game.

        Args:
            games (dict): The game data to be added.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the added game details.
        """
        existing_games = self.list_games({"event":games["event"]})
        for g in existing_games:
            if g["event"] == games["event"] and \
               g["start_time"] == games["start_time"] and \
               g["half"] == games["half"]:
                #print("WARNING: game already exists")
                return g

        return self.make_request("POST", "games", json=games, params=query_params)

    def change_games(self, id, games: dict, query_params=None):
        """
        Update an existing game.

        Args:
            id (int): The ID of the game to update.
            games (dict): The updated game data.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the updated game details.
        """
        return self.make_request("PATCH", f"games/{id}", json=games, params=query_params)

    def delete_games(self, id, query_params=None):
        """
        Delete a game.

        Args:
            id (int): The ID of the game to delete.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response confirming the deletion.
        """
        return self.make_request("DELETE", f"games/{id}", params=query_params)

    # Logs
    def list_robot_data(self, query_params=None):
        """
        List all logs.

        Args:
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the list of logs.
        """
        return self.make_request("GET", "robotdata", params=query_params)

    def get_robot_data(self, id, query_params=None):
        """
        Get a specific log.

        Args:
            id (int): The ID of the log.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the log details.
        """
        return self.make_request("GET", f"robotdata/{id}", params=query_params)

    def add_robot_data(self, log: dict, query_params=None):
        """
        Add a new log.

        Args:
            log (dict): The log data to be added.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the added log details.
        """
        return self.make_request("POST", "robotdata", json=log, params=query_params)

    def change_robot_data(self, id, log: dict, query_params=None):
        """
        Update an existing log.

        Args:
            id (int): The ID of the log to update.
            log (dict): The updated log data.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the updated log details.
        """
        return self.make_request("PATCH", f"robotdata/{id}", json=log, params=query_params)

    def delete_robot_data(self, id, query_params=None):
        """
        Delete a log.

        Args:
            id (int): The ID of the log to delete.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response confirming the deletion.
        """
        return self.make_request("DELETE", f"robotdata/{id}", params=query_params)

    # Image
    def list_images(self, query_params=None):
        """
        List all images.

        Args:
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the list of images.
        """
        return self.make_request("GET", "image", params=query_params)

    def get_image(self, id, query_params=None):
        """
        Get a specific image.

        Args:
            id (int): The ID of the image.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the image details.
        """
        return self.make_request("GET", f"image/{id}", params=query_params)

    def add_image(self, image: dict, query_params=None):
        """
        Add a new image.

        Args:
            image (dict): The image data to be added.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the added image details.
        """
        return self.make_request("POST", "image", json=image, params=query_params)

    def change_image(self, id, image: dict, query_params=None):
        """
        Update an existing image.

        Args:
            id (int): The ID of the image to update.
            image (dict): The updated image data.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the updated image details.
        """
        return self.make_request("PATCH", f"image/{id}", json=image, params=query_params)

    def delete_image(self, id, query_params=None):
        """
        Delete an image.

        Args:
            id (int): The ID of the image to delete.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response confirming the deletion.
        """
        return self.make_request("DELETE", f"image/{id}", params=query_params)

    def image_count(self, params):
        return self.make_request("GET", "api/image-count", params=params)
    

    # Image Annotation
    def list_imageannotations(self, query_params=None):
        """
        List all image annotations.

        Args:
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the list of image annotations.
        """
        return self.make_request("GET", "imageannotation", params=query_params)

    def get_imageannotation(self, id, query_params=None):
        """
        Get a specific image annotation.

        Args:
            id (int): The ID of the image annotation.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the image annotation details.
        """
        return self.make_request("GET", f"imageannotation/{id}", params=query_params)

    def add_imageannotation(self, annotation: dict, query_params=None):
        """
        Add a new image annotation.

        Args:
            annotation (dict): The image annotation data to be added.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the added image annotation details.
        """
        return self.make_request("POST", "imageannotation", json=annotation, params=query_params)

    def change_imageannotation(self, id, annotation: dict, query_params=None):
        """
        Update an existing image annotation.

        Args:
            id (int): The ID of the image annotation to update.
            annotation (dict): The updated image annotation data.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the updated image annotation details.
        """
        return self.make_request("PATCH", f"imageannotation/{id}", json=annotation, params=query_params)

    def delete_imageannotation(self, id, query_params=None):
        """
        Delete an image annotation.

        Args:
            id (int): The ID of the image annotation to delete.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response confirming the deletion.
        """
        return self.make_request("DELETE", f"imageannotation/{id}", params=query_params)
        


    def add_sensorlog_data(self, data: dict, query_params=None):
        """
        Add a new sensorlogs.

        Args:
            sensorlogs (dict): The sensorlogs data to be added.
            query_params (dict, optional): Additional query parameters.

        Returns:
            dict: The JSON response containing the added sensorlogs details.
        """
        return self.make_request("POST", "sensorlogs", json=data, params=query_params)