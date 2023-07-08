import cv2 as cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Setup mediapipe instance
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Curl counter variables
counter = 0
stage = 'Up'
instructions = "Start Training"
landmarksList = []
poseIsCorrect = False
bad_frames = 0


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
    fps = 30

    rotatedImage = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # (1) => flip on x-axis (skeleton flipped while drawing)
    flippedImage = cv2.flip(rotatedImage, 1)

    # Recolor image to RGB
    image = cv2.cvtColor(flippedImage, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Make detection
    results = pose.process(image)

    try:
        landmarks = results.pose_landmarks.landmark

        # get coordinates
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

        left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

        right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

        right_wrist = [0, 0]
        left_wrist = [0, 0]

        right_elbow = [0, 0]
        left_elbow = [0, 0]

        # List to Draw Skeleton
        landmarksList = [left_wrist, left_elbow, left_shoulder, left_hip,
                         left_knee, left_ankle, right_ankle, right_knee,
                         right_hip, right_shoulder, right_elbow, right_wrist]

        # calculate angles
        left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)

        right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)

        ankles_distance = np.sqrt(np.square(
            right_ankle[0] - left_ankle[0]) + np.square(right_ankle[1] - left_ankle[1]))
        
        
        # Curl counter logic
        if (left_knee_angle <= 85 and right_knee_angle <= 85) or ankles_distance < 0.3:

            bad_frames += 1
            poseIsCorrect = False

        else:

            bad_frames = 0
            poseIsCorrect = True

            if (left_knee_angle > 150 or right_knee_angle > 150) and stage == 'Down':

                counter += 1
                stage = 'Up'
                instructions = 'Bend your Knee'

            elif (left_knee_angle <= 90 or right_knee_angle <= 90) and (stage == 'Up') and (ankles_distance >= 0.3):
                
                stage = 'Down'
                instructions = 'Go Up'

            elif counter and counter % 5 == 0:

                instructions = 'Keep Going'

        bad_time = (1 / fps) * bad_frames

        if bad_time > 2:

            instructions = 'Widen your feet and align camera to your side'

    except:
        pass

    return image, counter, instructions, landmarksList, poseIsCorrect