import requests
import json

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
variables = None
data = {"query": query, "variables": variables}
default_headers = {"Accept": "application/json", "Content-Type": "application/json"}
req = requests.get("http://127.0.0.1:8000/graphql/", data=json.dumps(data).encode("utf-8"), headers=default_headers)

print(req.json())