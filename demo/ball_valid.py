"""
    Small demo showing what is possible with our new Visual Analytics Tool

    1. get all frames where option name path_striker2024 and forwardkick from behavior frame options
        => only return the frame numbers
    2. Use the frames as filter for Images (not implemented yet)
"""
from vaapi.client import Vaapi
import os


def demo2(client):
    response = client.xabsl_symbol.list(
        log_id=168,
        symbol_name="ball.team.is_valid",
        symbol_value="True"
    )

    print(f"Number of frames the team ball was valid: {len(response)}")

if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    demo2(client)