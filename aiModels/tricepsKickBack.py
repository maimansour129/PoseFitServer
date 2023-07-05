import cv2 as cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

counter = 0
stage = 'down'
instructions = ''
landmarksList = None
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
    global status
    global landmarksList
    global poseIsCorrect

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        
        x = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # (1) => flip on x-axis (skeleton flipped while drawing)
        flippedImage = cv2.flip(x, 1)

        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
    
        # Make detection
        results = pose.process(image)
    
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            
            # Get coordinates
            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
        
            
            # Calculate angle
            rep_angle = calculate_angle(shoulder, elbow, wrist)
            torso_arm_angle = calculate_angle(elbow, shoulder, hip)
            angle_hip = calculate_angle(shoulder, hip, knee)
            
            
            # counter logic
            if((angle_hip > 150) or (torso_arm_angle > 30)):
                # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                #                 mp_drawing.DrawingSpec(color=(255,0,0), thickness=4, circle_radius=2), 
                #                 mp_drawing.DrawingSpec(color=(0,0,255), thickness=4, circle_radius=2) 
                #                 )
                instructions = "Fix your Posture"
                poseIsCorrect = False
                
            if(angle_hip < 150) and (torso_arm_angle <= 30):

                poseIsCorrect = True

                # mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                #                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2), 
                #                 mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2) 
                #                 )

                instructions = "GO"
                if((rep_angle <= 90) and (stage == "Down")):
                    counter = counter+1
                    stage = "Up"
                if ((rep_angle >= 150) and (stage == "Up")):
                    stage = "Down"
            
        except:
            pass
        
    return image, counter, instructions, landmarksList, poseIsCorrect