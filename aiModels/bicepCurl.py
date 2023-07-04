import cv2 as cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# # Curl counter variables
counter = 0
status = None
stage = 'down'
instructions = None
landmarksList = None


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


def recieve_frame(frame):

    global counter
    global instructions
    global stage
    global status
    global landmarksList
    poseIsCorrect = False

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

        # (1) => flip on x-axis (skeleton flipped while drawing)
        flippedImagee = cv2.flip(frame, 1)

        # Recolor image to RGB
        image = cv2.cvtColor(flippedImagee, cv2.COLOR_BGR2RGB)
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

            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            
            # List to Draw Skeleton
            landmarksList = [left_wrist, left_elbow, left_shoulder, left_hip,
                             right_hip, right_shoulder, right_elbow, right_wrist]

            # Calculate angle
            left_torso_angle = calculate_angle(
                left_elbow, left_shoulder, left_hip)
            left_elbow_angle = calculate_angle(
                left_shoulder, left_elbow, left_wrist)

            right_torso_angle = calculate_angle(
                right_elbow, right_shoulder, right_hip)
            right_elbow_angle = calculate_angle(
                right_shoulder, right_elbow, right_wrist)

            # Visualize angle
            cv2.putText(image, str(left_elbow_angle),
                        tuple(np.multiply(left_elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
                                                        255, 255), 2, cv2.LINE_AA
                        )
            cv2.putText(image, "Torso: " + str(left_torso_angle),
                        tuple(np.multiply(left_elbow, [240, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,
                                                        255, 255), 2, cv2.LINE_AA
                        )

            # Curl counter logic

            if left_torso_angle > 20 or right_torso_angle > 20:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(
                                              color=(255, 0, 0), thickness=4, circle_radius=2),
                                          mp_drawing.DrawingSpec(
                                              color=(0, 0, 255), thickness=4, circle_radius=2)
                                          )
            else:
                poseIsCorrect = True

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(
                                              color=(245, 66, 230), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(
                                              color=(0, 255, 0), thickness=2, circle_radius=2)
                                          )
                if (left_elbow_angle < 30 and right_elbow_angle < 30) and stage == 'down':
                    stage = "up"
                    counter += 1
                    instructions = "Go Down"
                if ((left_elbow_angle < 160 and left_elbow_angle > 30) and (right_elbow_angle < 160 and right_elbow_angle > 30)) and stage == 'up':
                    instructions = "Go Down more"
                if left_elbow_angle >= 160 and right_elbow_angle >= 160 and stage == 'up':
                    stage = "down"
                    instructions = "Go Up"
                if ((left_elbow_angle > 30 and left_elbow_angle < 160) and (right_elbow_angle > 30 and right_elbow_angle < 160)) and stage == 'down':
                    instructions = "Go Up more"

            #Add bool in index 0 in skeleton list
            landmarksList.insert(0,poseIsCorrect)

        except:
            pass

    return image, counter, instructions,landmarksList