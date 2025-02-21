
import os
from vaapi.client import VATClient

client = VATClient(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
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

query = """
query{
images(filters:[{field:"log_id", value:"1"}, {field: "blurredness_value", value:null}]){
    frameNumber
    imageUrl
    blurrednessValue
  }
}
"""

b = client.execute(query)
print(b)