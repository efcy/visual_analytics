import os
from vaapi.client import VATClient


existing_logs = """
query{
  logs{id
  logPath}
}
"""
log_status = """
query log_status($id: String!) {
  logstatus(filters: [{ field: "log_id", value: $id }]) {
    logId {id}
    numJpgTop
    numJpgBottom
    numTop
    numBottom
  }
}
"""
log_status_var = {
  "id": "12"
}
#this would be cooler if it only returns fields that are null since this is what we are checking for in 05_calculate_num_frames is_done
log_status_cognition_frames = """query cognition_status($id: String!) {
  logstatus(filters: [{ field: "log_id", value: $id }]) {
    FrameInfo
    BallModel
    BallCandidates
    BallCandidatesTop
    CameraMatrix
    CameraMatrixTop
    FieldPercept
    FieldPerceptTop
    GoalPercept
    GoalPerceptTop
    MultiBallPercept
    RansacLinePercept
    RansacCirclePercept2018
    ShortLinePercept
    ScanLineEdgelPercept
    ScanLineEdgelPerceptTop
    OdometryData
    numCognitionFrames
  }
}"""
log_status_motion_frames = """
query cognition_status($id: String!){
logstatus(filters: [{ field: "log_id", value: $id }]){
    FrameInfo
    IMUData
    FSRData 
    ButtonData
    SensorJointData
    AccelerometerData
    InertialSensorData
    MotionStatus
    MotorJointData
    GyrometerData
    numMotionFrames
    }}
"""



if __name__ == "__main__":
    client = VATClient(
        base_url=os.environ.get("VAT_API_URL"),
        api_key=os.environ.get("VAT_API_TOKEN"),
    )

    data = client.execute(existing_logs,log_status_var)
    print(data)