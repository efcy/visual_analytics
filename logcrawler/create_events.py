
from vaapi.client import VATClient

client = VATClient(
    base_url="http://127.0.0.1:8000/",
    api_key="222ca62d70706ed2ff65afe21ca3475ff23f3b05",
)

query = """
query{
events {
    id
    name
  }
}
"""

create_query = """
mutation CreateEvent($name: String!) {
  bla(input: {name: $name})
    {
      name
  }
}
"""

a = client.execute(create_query, variables={"name": "aaaaaaaaaa"})
print(a)
b = client.execute(query)
print(b)