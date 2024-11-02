"""
"""
from vaapi.client import Vaapi
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


if __name__ == "__main__":
    client = Vaapi(
        base_url=os.environ.get("VAT_API_URL"),  
        api_key=os.environ.get("VAT_API_TOKEN"),
    )
    logs = client.logs.list()

    x_list = list()
    y_list = list()
    for data in logs:
        response = client.cognition_repr.list(
            log_id=1,
            representation_name='BallCandidatesTop',
        )
        print(len(response))

        for candidates in response:
            patch_list = candidates.representation_data["patches"]
            for patch in patch_list:
                mid_x = (patch["max"]["x"] + patch["min"]["x"]) / 2
                mid_y = (patch["max"]["y"] + patch["min"]["y"]) / 2
                x_list.append(mid_x)
                y_list.append(mid_y)
        break


    fig, ax = plt.subplots()
    plt.title('Frequency of Ball Percepts found in Image')
    h = ax.hist2d(x_list,y_list, bins=[np.arange(0,640,20),np.arange(0,480,20)])
    fig.colorbar(h[3], ax=ax)
    plt.savefig("abc.png")