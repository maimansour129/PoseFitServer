import cv2 as cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Setup mediapipe instance
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Curl counter variables
counter = 0
stage = 'down'
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

        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

        left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

        right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        # List to Draw Skeleton
        landmarksList = [left_wrist, left_elbow, left_shoulder, left_hip, left_knee, left_ankle, right_ankle, right_knee,
                         right_hip, right_shoulder, right_elbow, right_wrist]

        # Calculate angle
        left_arm_hip_angle = calculate_angle(
            left_elbow, left_shoulder, left_hip)

        right_arm_hip_angle = calculate_angle(
            right_elbow, right_shoulder, right_hip)

        knee_hip_angle = calculate_angle(left_ankle, left_hip, right_ankle)


        # Curl counter logic
        if (knee_hip_angle > 40):

            poseIsCorrect = False
            instructions = "Don't open leg too wide"

        if (knee_hip_angle <= 40):
            
            poseIsCorrect = True
            instructions = "Keep Going"

            if ((knee_hip_angle >= 10) and ((left_arm_hip_angle >= 70) and (right_arm_hip_angle >= 70)) and (stage == "Down")):
                counter += 1
                stage = "Up"
                instructions = "GO Up"

            if ((knee_hip_angle < 10) and ((left_arm_hip_angle < 70) and (right_arm_hip_angle < 70))) and stage == "Up":
                stage = "Down"
                instructions = "GO Down"

    except:
        pass

    return image, counter, instructions, landmarksList, poseIsCorrect
