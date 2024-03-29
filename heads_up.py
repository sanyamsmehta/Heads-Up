import cv2
import dlib
from scipy.spatial import distance
import os
from twilio.rest import Client

account_sid = '####' #Enter your Twilio account SID
auth_token = '####' #Enter your Twilio account Authentication Token
client = Client(account_sid, auth_token)
a = []
count = 0
flag = 0


def calculate_EAR(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear_aspect_ratio = (A+B)/(2.0*C)
    return ear_aspect_ratio


cap = cv2.VideoCapture(0)
address = "####" #Enter your own Webcam IP Address
cap.open(address)
hog_face_detector = dlib.get_frontal_face_detector()
dlib_facelandmark = dlib.shape_predictor(
    "shape_predictor_68_face_landmarks.dat")

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = hog_face_detector(gray)
    for face in faces:

        face_landmarks = dlib_facelandmark(gray, face)
        leftEye = []
        rightEye = []

        for n in range(36, 42):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
            leftEye.append((x, y))
            next_point = n+1
            if n == 41:
                next_point = 36
            x2 = face_landmarks.part(next_point).x
            y2 = face_landmarks.part(next_point).y
            cv2.line(frame, (x, y), (x2, y2), (0, 255, 0), 1)

        for n in range(42, 48):
            x = face_landmarks.part(n).x
            y = face_landmarks.part(n).y
            rightEye.append((x, y))
            next_point = n+1
            if n == 47:
                next_point = 42
            x2 = face_landmarks.part(next_point).x
            y2 = face_landmarks.part(next_point).y
            cv2.line(frame, (x, y), (x2, y2), (0, 255, 0), 1)

        left_ear = calculate_EAR(leftEye)
        right_ear = calculate_EAR(rightEye)

        EAR = (left_ear+right_ear)/2
        EAR = round(EAR, 2)
        if(EAR < 0.18):
            a.append(EAR)
            count += 1
            if(count > 2):
                call = client.calls.create(
                    twiml='<Response><Say>Stay Alert</Say></Response>', to='####', from_='####') #Enter mobile number you want to call and your Twilio Account registered mobile number.
                flag += 1
        else:
            count = 0
            a = []
            flag = 0

        if(flag == 1 or flag == 15):
            m = client.messages.create(
                to='####', from_='####', body="Enter message Body") #Enter cell phone number of emergency contact, Twilio account along with the message body.
        print(EAR)

        cv2.imshow("", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
