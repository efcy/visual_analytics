from vaapi.client import Vaapi
import os


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),  
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    """
    Get FrameInfo from Cognition Process
    """
    response = client.games.list(
        event_id= 1,
    )
    print(response)

    