import cv2 as cv2
import mediapipe as mp
import numpy as np
import math
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# # Curl counter variables
counter = 0
stage = 'down'
instructions = "Start training"
landmarksList = []
poseIsCorrect = False

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def receive_frame(frame):

    global counter
    global instructions
    global stage
    global landmarksList
    global poseIsCorrect

    # Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

        x = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # (1) => flip on x-axis (skeleton flipped while drawing)
        flippedImage = cv2.flip(x, 1)

        # Recolor image to RGB
        image = cv2.cvtColor(flippedImage, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Make detection
        results = pose.process(image)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            # Get coordinates
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            right_shoulder  = [0,0]
            right_elbow  = [0,0]
            right_wrist = [0,0]

            right_hip  = [0,0]
            right_knee = [0,0]
            right_ankle = [0,0]

            # List to Draw Skeleton
            landmarksList = [left_wrist, left_elbow, left_shoulder, left_hip,
                                left_knee, left_ankle, right_ankle, right_knee,
                                right_hip, right_shoulder, right_elbow, right_wrist]
            
            # Calculate angle            
            angle_knee = calculate_angle(left_hip, left_knee, left_ankle) #Knee joint angle
            
            angle_hip = calculate_angle(left_shoulder, left_hip, left_knee)
            
            # Visualize angle
            # cv2.putText(image, str(angle), 
            #                tuple(np.multiply(elbow, [640, 480]).astype(int)), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            #                     )
                       
                
            # cv2.putText(image, str(angle_knee), 
            #                tuple(np.multiply(knee, [640, 480]).astype(int)), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA
            #                     )
            
            # cv2.putText(image, str(angle_hip), 
            #                tuple(np.multiply(hip, [640, 480]).astype(int)), 
            #                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
            #                     )
            

            # Curl counter logic

            instructions = "Keep Going"

            if angle_hip > 55:
                instructions = "Goo"
                poseIsCorrect = True
                # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                #                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2), 
                #                 mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2) 
                #                  )

                if angle_knee < 135 and stage == 'Up':
                    instructions = "Go Down"
                    stage = "Down"
                    counter = counter+1

                if angle_knee >160 and stage == 'Down':
                    stage = "Up"
                    instructions = "Go Up"

            if angle_hip <= 80:
                # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                #                 mp_drawing.DrawingSpec(color=(255,0,0), thickness=4, circle_radius=2), 
                #                 mp_drawing.DrawingSpec(color=(0,0,255), thickness=4, circle_radius=2) 
                #                  )
                instructions = "Straighten your back"
                poseIsCorrect = False
            
        except:
            pass

    return image, counter, instructions, landmarksList, poseIsCorrect
