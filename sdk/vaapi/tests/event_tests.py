def basic_event_tests(client):
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
