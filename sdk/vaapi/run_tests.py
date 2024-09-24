from vaapi.client import Vaapi
from tests.event_tests import basic_event_tests
from tests.logs_tests import basic_log_tests

if __name__ == "__main__":
    client = Vaapi(
        base_url='http://127.0.0.1:8000/',  
        api_key="84c6f4b516cc9d292f1b0eba26ea88e99812fbb9",
    )
    a = client.annotations.get(id=1)
    print(a)

    basic_event_tests(client)
    print()
    basic_log_tests(client)
