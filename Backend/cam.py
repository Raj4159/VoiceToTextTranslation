# from ultralytics import YOLO
import cv2
import mediapipe as mp
import numpy as np

from models import User
import jwt
from dotenv import load_dotenv
import os
from mongoengine import connect

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

connect("fluency", host="localhost", port=27017) #connecting to the database

def add_warning(token: str):
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = decoded_token.get("sub")

    # Find the user by username
    user = User.objects.get(username=username)

    # Increment warning count
    user.warnings += 1
    user.save()



x = 0                                       # X axis head pose
y = 0                                       # Y axis head pose

X_AXIS_CHEAT = 0
Y_AXIS_CHEAT = 0

PLOT_LENGTH = 200

frame_counter = 0

# place holders 
GLOBAL_CHEAT = 0
PERCENTAGE_CHEAT = 0
CHEAT_THRESH = 0.6
XDATA = list(range(200))
YDATA = [0]*200

def avg(current, previous):
    if previous > 1:
        return 0.65
    if current == 0:
        if previous < 0.01:
            return 0.01
        return previous / 1.01
    if previous == 0:
        return current
    return 1 * previous + 0.1 * current

def process(token):
    global GLOBAL_CHEAT, PERCENTAGE_CHEAT, CHEAT_THRESH, frame_counter
    if GLOBAL_CHEAT == 0:
        if X_AXIS_CHEAT == 0:
            if Y_AXIS_CHEAT == 0:
                PERCENTAGE_CHEAT = avg(0, PERCENTAGE_CHEAT)
            else:
                PERCENTAGE_CHEAT = avg(0.15, PERCENTAGE_CHEAT)
        else:
            if Y_AXIS_CHEAT == 0:
                PERCENTAGE_CHEAT = avg(0.1, PERCENTAGE_CHEAT)
            else:
                PERCENTAGE_CHEAT = avg(0.25, PERCENTAGE_CHEAT)
    else:
        if X_AXIS_CHEAT == 0:
            if Y_AXIS_CHEAT == 0:
                PERCENTAGE_CHEAT = avg(0, PERCENTAGE_CHEAT)
            else:
                PERCENTAGE_CHEAT = avg(0.55, PERCENTAGE_CHEAT)
        else:
            if Y_AXIS_CHEAT == 0:
                PERCENTAGE_CHEAT = avg(0.6, PERCENTAGE_CHEAT)
            else:
                PERCENTAGE_CHEAT = avg(0.85, PERCENTAGE_CHEAT)


    if PERCENTAGE_CHEAT > CHEAT_THRESH:
        GLOBAL_CHEAT = 1
        frame_counter += 1
        if frame_counter > 120:
            frame_counter = 0
            add_warning(token)
            print("CHEATING")


def pose(token : str):
    global VOLUME_NORM, x, y, X_AXIS_CHEAT, Y_AXIS_CHEAT
    #############################
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)
    mp_drawing = mp.solutions.drawing_utils
    # mp_drawing_styles = mp.solution


    while cap.isOpened():
        success, image = cap.read()
        
        if not success:
            print("something went wrong")
            break
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance
        image.flags.writeable = False
        
        # Get the result
        results = face_mesh.process(image)
        
        # To improve performance
        image.flags.writeable = True
        
        # Convert the color space from RGB to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = image.shape
        face_3d = []
        face_2d = []
        
        face_ids = [33, 263, 1, 61, 291, 199]

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None)
                for idx, lm in enumerate(face_landmarks.landmark):
                    # print(lm)
                    if idx in face_ids:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        # Get the 2D Coordinates
                        face_2d.append([x, y])

                        # Get the 3D Coordinates
                        face_3d.append([x, y, lm.z])       
                
                # Convert it to the NumPy array
                face_2d = np.array(face_2d, dtype=np.float64)

                # Convert it to the NumPy array
                face_3d = np.array(face_3d, dtype=np.float64)

                # The camera matrix
                focal_length = 1 * img_w

                cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                        [0, focal_length, img_w / 2],
                                        [0, 0, 1]])

                # The Distance Matrix
                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                # Solve PnP
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                # Get rotational matrix
                rmat, jac = cv2.Rodrigues(rot_vec)

                # Get angles
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                # Get the y rotation degree
                x = angles[0] * 360
                y = angles[1] * 360

                # print(y)
                process(token)

                # See where the user's head tilting
                if y < -10:
                    text = "Looking Left"
                elif y > 10:
                    text = "Looking Right"
                elif x < -10:
                    text = "Looking Down"
                else:
                    text = "Forward"
                text = str(int(x)) + "::" + str(int(y)) + text
                # print(str(int(x)) + "::" + str(int(y)))
                # print("x: {x}   |   y: {y}  |   sound amplitude: {amp}".format(x=int(x), y=int(y), amp=audio.SOUND_AMPLITUDE))
                
                # Y is left / right
                # X is up / down
                if y < -10 or y > 10:
                    X_AXIS_CHEAT = 1
                    # print("X_AXIS_CHEAT: ", X_AXIS_CHEAT)
                else:
                    X_AXIS_CHEAT = 0
                    # print("X_AXIS_CHEAT: ", X_AXIS_CHEAT)
                if x < -5:
                    Y_AXIS_CHEAT = 1
                    # print("Y_AXIS_CHEAT: ", Y_AXIS_CHEAT)
                else:
                    Y_AXIS_CHEAT = 0
                    # print("Y_AXIS_CHEAT: ", Y_AXIS_CHEAT)

                # print(X_AXIS_CHEAT, Y_AXIS_CHEAT)
                # Display the nose direction
               
                nose_3d_projection, jacobian = cv2.projectPoints(nose_3d, rot_vec, trans_vec, cam_matrix, dist_matrix)


                p1 = (int(nose_2d[0]), int(nose_2d[1]))
                p2 = (int(nose_3d_projection[0][0][0]), int(nose_3d_projection[0][0][1]))
                
                cv2.line(image, p1, p2, (255, 0, 0), 2)

                # Add the text on the image
                cv2.putText(image, text, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.imshow("fluency", image)
        
        # check for a person and a cell phone using YOLO
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()

#############################
if __name__ == "__main__":
    print("Running...")
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE3MTM0NDU1NTB9.2ZcwwQSlZ8D454xgUs949cDz1Z26TvYSoJH4FKr4A2s"
    pose(token)
    
    # print(x, y, X_AXIS_CHEAT, Y_AXIS_CHEAT)
