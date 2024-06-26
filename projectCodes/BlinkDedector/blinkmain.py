import socket
import cv2 as cv
import mediapipe as mp
import time
import utils
import math
import numpy as np

# UDP Server setup
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSocket.bind(("localhost", 12000))

# Variables
frame_counter = 0
CEF_COUNTER_LEFT = 0
CEF_COUNTER_RIGHT = 0
TOTAL_BLINKS = 0
validLeft = 10.0
validRight = 10.0
last_blink_time = 1

lastOne=[]
# Constants
CLOSED_EYES_FRAME = 3
FONTS = cv.FONT_HERSHEY_COMPLEX
BLINK_COOLDOWN = 0  # 2 seconds

# Left and right eyes indices
LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

map_face_mesh = mp.solutions.face_mesh
camera = cv.VideoCapture(0)

# Landmark detection function
def landmarksDetection(img, results, draw=False):
    img_height, img_width = img.shape[:2]
    mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.multi_face_landmarks[0].landmark]
    if draw:
        [cv.circle(img, p, 2, (0, 255, 0), -1) for p in mesh_coord]
    return mesh_coord

# Euclidean distance
def euclideanDistance(point, point1):
    x, y = point
    x1, y1 = point1
    distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)
    return distance

# Blinking ratio
def blinkRatio(img, landmarks, indices):
    right_point = landmarks[indices[0]]
    left_point = landmarks[indices[8]]
    top_point = landmarks[indices[12]]
    bottom_point = landmarks[indices[4]]
    hor_distance = euclideanDistance(right_point, left_point)
    ver_distance = euclideanDistance(top_point, bottom_point)
    return hor_distance / ver_distance

# Callback function for trackbar (do nothing)
def nothing(x):
    pass

# Create a window for trackbars and video
cv.namedWindow('Blink Detector')
cv.createTrackbar('Valid Left', 'Blink Detector', 40, 60, nothing)
cv.createTrackbar('Valid Right', 'Blink Detector', 40, 60, nothing)

with map_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
    start_time = time.time()
    while True:
        frame_counter += 1
        ret, frame = camera.read()
        if not ret:
            break

        # Read trackbar positions
        validLeft = cv.getTrackbarPos('Valid Left', 'Blink Detector') / 10
        validRight = cv.getTrackbarPos('Valid Right', 'Blink Detector') / 10

        frame = cv.resize(frame, None, fx=1.5, fy=1.5, interpolation=cv.INTER_CUBIC)
        frame_height, frame_width = frame.shape[:2]
        rgb_frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        results = face_mesh.process(rgb_frame)

        if results.multi_face_landmarks:
            mesh_coords = landmarksDetection(frame, results, False)
            ratioLeft = blinkRatio(frame, mesh_coords, LEFT_EYE)
            ratioRight = blinkRatio(frame, mesh_coords, RIGHT_EYE)

            utils.colorBackgroundText(frame, f'Ratio Left : {round(ratioLeft, 2)}', FONTS, 0.7, (30, 100), 2, utils.PINK, utils.YELLOW)
            utils.colorBackgroundText(frame, f'Ratio Right : {round(ratioRight, 2)}', FONTS, 0.7, (30, 130), 2, utils.PINK, utils.YELLOW)

            current_time = time.time()
            if current_time - last_blink_time > BLINK_COOLDOWN:
                if ratioLeft > 5 and ratioRight > 5:
                    CEF_COUNTER_LEFT += 1
                    CEF_COUNTER_RIGHT += 1
                    utils.colorBackgroundText(frame, 'Blink Both', FONTS, 1.7, (int(frame_width / 2), 100), 2, utils.YELLOW, pad_x=6, pad_y=6)
                elif ratioRight > validRight:
                    CEF_COUNTER_RIGHT += 1
                    utils.colorBackgroundText(frame, 'Blink Right', FONTS, 1.7, (int(frame_width / 2), 100), 2, utils.YELLOW, pad_x=6, pad_y=6)
                elif ratioLeft > validLeft:
                    CEF_COUNTER_LEFT += 1
                    utils.colorBackgroundText(frame, 'Blink Left', FONTS, 1.7, (int(frame_width / 2), 100), 2, utils.YELLOW, pad_x=6, pad_y=6)
                else:
                    if CEF_COUNTER_LEFT > CLOSED_EYES_FRAME:
                        TOTAL_BLINKS += 1
                        CEF_COUNTER_LEFT = 0
                        last_blink_time = current_time  # Update last blink time
                        secimmmm = 0
                        message, clientAddress = serverSocket.recvfrom(1024)
                        serverSocket.sendto(str(secimmmm).encode(), clientAddress)  # UDP client 0 gönder
                    elif CEF_COUNTER_RIGHT > CLOSED_EYES_FRAME:
                        TOTAL_BLINKS += 1
                        CEF_COUNTER_RIGHT = 0
                        last_blink_time = current_time  # Update last blink time
                        secimmmm = 1
                        message, clientAddress = serverSocket.recvfrom(1024)
                        serverSocket.sendto(str(secimmmm).encode(), ('localhost', 12000))  # UDP client 1 gönder
                    elif ratioLeft > 5 and ratioRight > 5:
                        secimmmm = 2
                        message, clientAddress = serverSocket.recvfrom(1024)
                        serverSocket.sendto(str(secimmmm).encode(), ('localhost', 12000))  # UDP client 2 gönder

            utils.colorBackgroundText(frame, f'Total Blinks: {TOTAL_BLINKS}', FONTS, 0.7, (30, 160), 2)
            cv.polylines(frame, [np.array([mesh_coords[p] for p in LEFT_EYE], dtype=np.int32)], True, utils.GREEN, 1, cv.LINE_AA)
            cv.polylines(frame, [np.array([mesh_coords[p] for p in RIGHT_EYE], dtype=np.int32)], True, utils.GREEN, 1, cv.LINE_AA)

        end_time = time.time() - start_time
        fps = frame_counter / end_time
        frame = utils.textWithBackground(frame, f'FPS: {round(fps, 1)}', FONTS, 1.0, (30, 50), bgOpacity=0.9, textThickness=2)

        cv.imshow('Blink Detector', frame)
        key = cv.waitKey(2)
        if key == ord('q') or key == ord('Q'):
            break

    cv.destroyAllWindows()
    camera.release()
serverSocket.close()