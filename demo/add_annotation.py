"""
"""
from vaapi.client import Vaapi
import os


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    

    result = client.annotation.get(id=3389974)
    print(result)
    """
    {
    "bbox": [
        {
            "id": 123,
            "x": 0,
            "y": 0,
            "width": 100,
            "height": 100,
            "label": "ball",
            "creator": "username-bot",
            "created": "a",
            "modified": "a"
        }
    ]
}
    """