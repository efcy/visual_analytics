from vaapi.client import Vaapi
import os


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),  
        api_key="222ca62d70706ed2ff65afe21ca3475ff23f3b05",
    )
    """
    Get FrameInfo from Cognition Process
    """
    response = client.games.list(
        event_id= 1,
    )
    print(response)

    