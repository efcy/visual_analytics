import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import classes from "./DataView.module.css";

const DataView = () => {
  return (
    <div className={classes.representationSelector}>
      <Tabs className={classes.tabsContainer}>
        <TabsList className={`grid h-full grid-rows`}>
          <TabsTrigger value="Representations" className={classes.verticalButton}>Representations</TabsTrigger>
          <TabsTrigger value="Annotations" className={classes.verticalButton}>Annotations</TabsTrigger>
          <TabsTrigger value="Comments" className={classes.verticalButton}>Comments</TabsTrigger>
        </TabsList>
        <TabsContent value="Representations" className={classes.tabsContent}>
          <Tabs
            defaultValue="MultiBallPercept"
            className={classes.tabsContainer}
          >
            <TabsList className={`grid h-full grid-rows ${classes.tabsList}`}>
              <TabsTrigger value="MultiBallPercept">
                MultiBallPercept
              </TabsTrigger>
              <TabsTrigger value="BallModel">BallModel</TabsTrigger>
              <TabsTrigger value="TeamState">TeamState</TabsTrigger>
              <TabsTrigger value="ScanLineEdgelPercept">
                ScanLineEdgelPercept
              </TabsTrigger>
              <TabsTrigger value="FSRData">FSRData</TabsTrigger>
              <TabsTrigger value="BallCandidatesTop">
                BallCandidatesTop
              </TabsTrigger>
              <TabsTrigger value="CameraMatrixTop">CameraMatrixTop</TabsTrigger>
              <TabsTrigger value="TeamMessageDecision">
                TeamMessageDecision
              </TabsTrigger>
              <TabsTrigger value="MotionStatus">MotionStatus</TabsTrigger>
              <TabsTrigger value="ShortLinePercept">
                ShortLinePercept
              </TabsTrigger>
              <TabsTrigger value="RansacLinePercept">
                RansacLinePercept
              </TabsTrigger>
              <TabsTrigger value="ScanLineEdgelPerceptTop">
                ScanLineEdgelPerceptTop
              </TabsTrigger>
              <TabsTrigger value="InertialSensorData">
                InertialSensorData
              </TabsTrigger>
              <TabsTrigger value="RobotInfo">RobotInfo</TabsTrigger>
              <TabsTrigger value="GoalPercept">GoalPercept</TabsTrigger>
              <TabsTrigger value="FieldPerceptTop">FieldPerceptTop</TabsTrigger>
              <TabsTrigger value="MotorJointData">MotorJointData</TabsTrigger>
              <TabsTrigger value="CameraMatrix">CameraMatrix</TabsTrigger>
              <TabsTrigger value="SensorJointData">SensorJointData</TabsTrigger>
              <TabsTrigger value="ButtonData">ButtonData</TabsTrigger>
              <TabsTrigger value="RansacCirclePercept2018">
                RansacCirclePercept2018
              </TabsTrigger>
              <TabsTrigger value="FieldPercept">FieldPercept</TabsTrigger>
              <TabsTrigger value="AudioData">AudioData</TabsTrigger>
              <TabsTrigger value="GoalPerceptTop">GoalPerceptTop</TabsTrigger>
              <TabsTrigger value="BallCandidates">BallCandidates</TabsTrigger>
              <TabsTrigger value="OdometryData">OdometryData</TabsTrigger>
              <TabsTrigger value="FrameInfo">FrameInfo</TabsTrigger>
              <TabsTrigger value="AccelerometerData">
                AccelerometerData
              </TabsTrigger>
              <TabsTrigger value="IMUData">IMUData</TabsTrigger>
              <TabsTrigger value="GyrometerData">GyrometerData</TabsTrigger>
            </TabsList>
            <TabsContent
              value="MultiBallPercept"
              className={classes.tabsContent}
            >
              MultiBallPercept Data
            </TabsContent>
            <TabsContent value="GyrometerData">
              Change your password here.
            </TabsContent>
          </Tabs>
        </TabsContent>
        <TabsContent value="Annotations" className={classes.tabsContent}>
          Annotations
        </TabsContent>
        <TabsContent value="Comments" className={classes.tabsContent}>
          Comments
        </TabsContent>
      </Tabs>
    </div>
  );
};
export default DataView;
