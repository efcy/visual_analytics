
import os
from vaapi.client import VATClient

client = VATClient(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
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
        id
        name
    }
}
"""

a = client.execute(create_query, variables={"name": "2024-07-15_RC24"})
print(a)
b = client.execute(query)
print(b)