import cv2 as cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def recieve_frame(frame):
    counter = 0 
    status = None
    stage = 'down'
    instructions=None
    flag=0
    feedback_text= None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            
            left_ankel = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            #left_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
            
            #left_heel_index = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
            
            if flag == 0:
                left_arch = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                #left_heel_vert = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
                flag = 1
                
            # Calculate angles
            
            left_knee_angle = calculate_angle(left_hip, left_knee, left_ankel)
            left_shoulder_angle = calculate_angle(left_elbow, left_shoulder, left_hip)
            left_arch_angle = calculate_angle(left_shoulder, left_hip, left_arch)
            #left_heel_angle = calculate_angle(left_heel_index, left_heel_vert, left_heel)
            
            # Visualize angle
            cv2.putText(image, str(left_shoulder_angle), 
                           tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, "Knee: " + str(left_knee_angle), 
                           tuple(np.multiply(left_elbow, [240, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
            # Curl counter logic
            
            #if left_shoulder_angle < 70 :
                #mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                #mp_drawing.DrawingSpec(color=(255,0,0), thickness=4, circle_radius=2), 
                                #mp_drawing.DrawingSpec(color=(0,0,255), thickness=4, circle_radius=2) 
                                 #)
            
            ##########-------Checking Back Pose-----##############
            if left_arch_angle > 35:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(255,0,0), thickness=4, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(0,0,255), thickness=4, circle_radius=2) 
                                 )
                feedback_text = "Straighten your Back!"
                
            ##########-----Checking Heel Pose--------#########  
#             elif left_heel_vert > 20:
#                 mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#                                 mp_drawing.DrawingSpec(color=(255,0,0), thickness=4, circle_radius=2), 
#                                 mp_drawing.DrawingSpec(color=(0,0,255), thickness=4, circle_radius=2) 
#                                  )
#                 feedback_text = "Heel to Ground!"
            else:
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2) 
                                 )
                feedback_text = "Good Work!"
                if (left_knee_angle > 170) and stage == 'down':
                    stage = "up"
                    #counter += 1
                    #instructions = "Go Down"
                if (left_knee_angle < 110) and stage =='up':
                    stage = "down"
                    counter+=1
              
                       
        except:
            pass
        
        return image, counter, feedback_text