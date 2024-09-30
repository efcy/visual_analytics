# test list function with filtering on the logs as an example
from vaapi.client import Vaapi
import os


if __name__ == "__main__":
    client = Vaapi(
        base_url='https://api.berlin-united.com/',  
        #FIXME use env var here
        api_key="43378af71b0af6b8064b61ce13ac8bbab42ed151",
    )
    client = Vaapi(
        base_url='http://127.0.0.1:8000/',  
        #FIXME use env var here
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    # TODO build another filter that filters the fields that are returned
    response = client.behavior_frame_option.list(log_id=7)
    #print(len(response))
    my_list = [None] * len(response)
    for idx, data in enumerate(response):

        my_list[idx] = data.frame
    #expectedResult = [d.frame for d in response if d.frame in response]
    print(len(set(my_list)))
    #print(len(expectedResult))
    #print(expectedResult[0])
