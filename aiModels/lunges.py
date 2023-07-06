import cv2 as cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# # Curl counter variables
counter = 0
stage = 'up'
instructions = "Start training"
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

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

        x = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # (1) => flip on x-axis (skeleton flipped while drawing)
        flippedImage = cv2.flip(x, 1)

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

            right_wrist = [0, 0]
            left_wrist = [0, 0]

            right_elbow = [0, 0]
            left_elbow = [0, 0]

            right_shoulder = [0, 0]
            left_shoulder = [0, 0]

            # List to Draw Skeleton
            landmarksList = [left_wrist, left_elbow, left_shoulder, left_hip,
                                left_knee, left_ankle, right_ankle, right_knee,
                                right_hip, right_shoulder, right_elbow, right_wrist]

            # calculate angles
            left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
            right_knee_angle = calculate_angle(
                right_hip, right_knee, right_ankle)

            ankles_distance = np.sqrt(np.square(
                right_ankle[0] - left_ankle[0]) + np.square(right_ankle[1] - left_ankle[1]))

            # cv2.putText(image, "left knee: " + str(left_knee_angle),
            #                tuple(np.multiply(left_knee, [300, 280]).astype(int)),
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            #                     )

            # cv2.putText(image, "right knee: " + str(right_knee_angle),
            #                tuple(np.multiply(right_knee, [240, 480]).astype(int)),
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            #                     )

            # cv2.putText(image, "distance: " + str(ankles_distance),
            #                tuple([360, 600].astype(int)),
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            #                     )

            if (left_knee_angle <= 85 and right_knee_angle <= 85) or ankles_distance < 0.3:
                # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                #                           mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=4, circle_radius=2),
                #                           mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=4, circle_radius=2)
                #                           )
                bad_frames += 1
                poseIsCorrect = False

            else:
                bad_frames = 0
                poseIsCorrect = True
                # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                #                           mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=4, circle_radius=2),
                #                           mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=4, circle_radius=2)
                #                           )

                if (left_knee_angle > 150 or right_knee_angle > 150) and stage == 'down':
                    counter += 1
                    stage = 'up'
                    instructions = 'Bend your Knee'

                elif (left_knee_angle <= 90 or right_knee_angle <= 90) and (stage == 'up') and (ankles_distance >= 0.3):
                    stage = 'down'
                    instructions = 'Go Up'
                elif counter and counter % 5 == 0:
                    instructions = 'Keep Going'

            bad_time = (1 / fps) * bad_frames

            if bad_time > 2:
                instructions = 'Widen your feet and align the camera to your side'

        except:
            pass

    return image, counter, instructions, landmarksList, poseIsCorrect

    # Setup status box
    # cv2.rectangle(image, (0,0), (550,50), (245,117,16), -1)

    # cv2.putText(image,"Reps: " + str(counter),
    #             (10, 40),
    #             cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 4, cv2.LINE_AA)
    # cv2.putText(image,str(instructions),
    #             (300, 40),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 3, cv2.LINE_AA)
