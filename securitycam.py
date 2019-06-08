from time import sleep
import camm
import cv2
from cv2 import face
import time
import gmail

######
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
######
cam = cv2.VideoCapture(0)

def activityDetection():
    key = 1
    while True:
        print("detection is workin")
        ret, im = cam.read()
        if key == 1:
            control = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("motion/control.jpg",control)
            cv2.imwrite("motion/now.jpg", im)
            key = 0
        #ret, im2 = cam.read()
        #cv2.imshow("Video", im2)
        cv2.imwrite("motion/now.jpg", im)
        now = cv2.imread("motion/now.jpg", 0)
        similarity = cv2.matchTemplate(control, now, cv2.TM_CCOEFF_NORMED)
        print("Similarity:  " + str(similarity[0][0]))
        if (similarity[0][0] >= 0.93):
            print("Safe")
            #list.append(0)
        else:
            print("Odada Hareket tespit edildi")
            cv2.imwrite("motion/UFO.jpg",now)
            ########
            confirmation = 0
            unknownCounter = 0
            w = time.time()
            q = w
            print("cam is working")
            while True:
                ret, im = cam.read()
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                    Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                    if (conf < 50):
                        print(camm.user(Id))
                        name = camm.user(Id)
                        if camm.user(Id) == camm.user(Id):
                            confirmation = confirmation + 1
                    else:
                        Id = 0
                        name = "Unknown"
                        unknownCounter = unknownCounter + 1
                        print("Unknown")
                        ##time.sleep(1)
                    cv2.putText(im, str(name), (x, y + h), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 2)
                ##cv2.imshow('SecurityCam',im)
                if confirmation >= 10 and str(camm.user(Id)) == camm.user(Id):
                    print("You are " + camm.user(Id))
                    print(time.time() - q)
                    print("cam stop")
                    break
                elif unknownCounter >= 50:
                    print("I don't know you!")
                    calendar = str(time.localtime()[0]) + "." + str(time.localtime()[1]) + "." + str(time.localtime()[2])
                    cv2.imwrite("unknown/" + calendar + ".jpg",im)
                    gmail.send_mail(calendar)
                    print("cam stop")
                    break
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            ########
        print("detection sleep for 10 seconds")
        sleep(10)



activityDetection()