
from vaapi.client import VATClient

client = VATClient(
    base_url="http://127.0.0.1:8000/",
    api_key="222ca62d70706ed2ff65afe21ca3475ff23f3b05",
)

query = """
query{
logstatus(filters:[{field:"log_id", value:"2"}]){
    FrameInfo
    BallModel
  }
}
"""

query = """
query{
cogrepr(filters:[{field:"log_id", value:"1"}, {field: "representation_name", value:"FieldPercept"}]){
    representationData
  }
}
"""

b = client.execute(query)
print(b)