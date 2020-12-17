from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import cv2
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# arguments for user friendliness
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
                help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
                help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.25,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())


Classes = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

# draw samples from a uniform distribution of colors to set to each class's bounding box
# numpy.random.uniform(low, high, size)
Colors = np.random.uniform(0, 255, size=(len(Classes), 3))

# load prototxt and the caffe model
print("[INFO] loading model...")

# Now I can build the CNN (network) with the files prototxt and caffemodel in path
# using the cv2.dnn() module I can use the method where I read from Caffe
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

#start up the pi camera stream and read frames ps
print("[INFO] starting video stream...")
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
fps = FPS().start()

# connect to the drone through a udp connection (port 14550)
print("Connecting to vehicle...")
vehicle = connect('0.0.0.0:14550', wait_ready=True)


# Function to arm and then takeoff to a user specified altitude
def takeoff_drone(aTargetAltitude):
    print("Doing Pre-Arm checks...")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for drone to get ready...")
        time.sleep(1)

    print("Arming motors...")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Drone is arming...")
        time.sleep(1)

    # Take off to target altitude
    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)

    # Check that vehicle has reached takeoff altitude
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break from function if current altitude is >= target altitude
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0$
            print("Target Reached!!")
            break
        time.sleep(1)


def object_detection():
    while True:
        # main loop
        # read frames and resize each to the exact same dimensions
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # Slice the dimensions of the frame to get height and width
        # produce a blob from the input frames
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)

        # blob is the input into the CNN producing the output detections
        # detections is what the CNN forwards / outputs from the blob
        net.setInput(blob)
        detections = net.forward()

        # looping through the detections again with the .shape() attribute to return the dimensions
        for i in np.arange(0, detections.shape[2]):

            # get confidence of detection from the array
            confidence = detections[0, 0, i, 2]


            # if confidence of the detection is greater than the default confidence argument then run
            # have a 25% threshold for detections
            if confidence > args["confidence"]:

                # idx is the class label of the detection
                # multiply the detection array with the width and height array
                # produce a bounding box of type int with the coordinates produced as the multiple of the detection
                idx = int(detections[0, 0, i, 1])
                print("Detected: ", Classes[idx])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])


                # These will all be string values hence get them as integers
                (startX, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(Classes[idx],
                                             confidence * 100)

                # draw the box around the object
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                              Colors[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, Colors[idx], 2)
                # If a certain object is seen stop flying...
                if idx == 1:
                    print("Detected: ", Classes[idx])
                    break



        # if the q is pressed break loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        # update the FPS counter
        fps.update()


        # cleanup
        cv2.destroyAllWindows()
        vs.stop()
    return True


# Take off to 5m and land if object 8 is detected.
takeoff_drone(5)
if object_detection():
    print("Take off complete")

    # Hover for 10 seconds
    time.sleep(10)

    print("Now let's land")
    vehicle.mode = VehicleMode("LAND")

    # Close vehicle object
    vehicle.close()
