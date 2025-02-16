import requests
import json
import os

class VATClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def execute(self, query):
        default_headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Token {self.api_key}"}
        data = {"query": query}
        req = requests.get(f"{self.base_url}graphql/", data=json.dumps(data).encode("utf-8"), headers=default_headers)
        print(req.json())

1
client = VATClient(
    base_url=os.environ.get("VAT_API_URL"),
    api_key=os.environ.get("VAT_API_TOKEN"),
)

query = """
query{
events {
    id
    name
    games{
      id
      team1
      team2
    }
  }
}
"""
client.execute(query)

