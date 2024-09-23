from vaapi.client import Vaapi

if __name__ == "__main__":
    client = Vaapi(
    base_url='http://127.0.0.1:8000/',  
    api_key="84c6f4b516cc9d292f1b0eba26ea88e99812fbb9",
)
    a = client.events.create(name="test_event")
    print(a)

    b = client.events.get(id=a.id)
    print(b)

    c = client.events.list()
    print(c) 

    d = client.events.update(a.id, name="test_event_renamed")
    print(d)
    
    e = client.events.delete(a.id)
    print(e)
