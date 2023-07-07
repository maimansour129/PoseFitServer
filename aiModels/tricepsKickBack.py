import cv2 as cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Setup mediapipe instance
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Curl counter variables
counter = 0
stage = 'Down'
instructions = "Start Training"
landmarksList = []
poseIsCorrect = False


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
        np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle


def receive_frame(frame):

    global counter
    global instructions
    global stage
    global landmarksList
    global poseIsCorrect

    rotatedImage = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # (1) => flip on x-axis (skeleton flipped while drawing)
    flippedImage = cv2.flip(rotatedImage, 1)

    # Recolor image to RGB
    image = cv2.cvtColor(flippedImage, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Make detection
    results = pose.process(image)

    # Extract landmarks
    try:
        landmarks = results.pose_landmarks.landmark

        # Get coordinates
        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        right_shoulder = [0, 0]
        right_elbow = [0, 0]
        right_wrist = [0, 0]

        right_hip = [0, 0]
        right_knee = [0, 0]
        right_ankle = [0, 0]

        # Calculate angle
        rep_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        torso_arm_angle = calculate_angle(left_elbow, left_shoulder, left_hip)
        angle_hip = calculate_angle(left_shoulder, left_hip, left_knee)

        # List to Draw Skeleton
        landmarksList = [left_wrist, left_elbow, left_shoulder, left_hip,
                         left_knee, left_ankle, right_ankle, right_knee,
                         right_hip, right_shoulder, right_elbow, right_wrist]


        # counter logic
        if ((angle_hip > 150) or (torso_arm_angle > 20)):

            instructions = "Fix your Posture"
            poseIsCorrect = False

        if (angle_hip < 150) and (torso_arm_angle <= 20):

            poseIsCorrect = True

            if ((rep_angle <= 90) and (stage == "Down")):

                counter = counter+1
                stage = "Up"
                instructions = "Go Up"

            elif ((rep_angle >= 150) and (stage == "Up")):
                stage = "Down"
                instructions = "Go Down"
            
            elif counter and counter % 5 == 0:
                instructions = 'Keep Going'
    except:
        pass

    return image, counter, instructions, landmarksList, poseIsCorrect