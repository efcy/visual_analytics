from vaapi.client import Vaapi
import os


def frame_filter_demo(client):
    response = client.behavior_frame_option.filter(
        log_id=168,
        option_name="path_striker2024",
        state_name="forwardkick",
    )

    resp = client.frame_filter.create(
        log_id=168,
        frames={"frame_list": response},
    )


if __name__ == "__main__":
    client = Vaapi(
        base_url='http://127.0.0.1:8000/',  
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    frame_filter_demo(client)