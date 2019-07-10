import cv2
from cv2 import face
import xlrd
import time

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

def user(id):
    rb = xlrd.open_workbook('users.xls')
    worksheet = rb.sheet_by_index(0)
    name = worksheet.cell(0,int(id)).value
    return name


def scam(list2):
    cam = cv2.VideoCapture(0)
    confirmation = 0
    unknownCounter = 0
    w = time.time()
    q = w
    print("cam is working")
    list2.append(1)
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            if(conf<50):
                print(user(Id))
                name = user(Id)
                if user(Id) == "Talha":
                    confirmation = confirmation + 1
            else:
                Id = 0
                name="Unknown"
                unknownCounter = unknownCounter + 1
                print("Unknown")
                ##time.sleep(1)
            cv2.putText(im, str(name), (x,y+h), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 2)
        ##cv2.imshow('SecurityCam',im)
        if confirmation >= 10 and str(user(Id)) == "Talha":
            print("You are " + user(Id))
            print(time.time() - q)
            print("cam stop")
            list2.append(0)
            break
        elif unknownCounter >= 50:
            print("I don't know you!")
            print("fotoğraf çekmesi gerekiyor")
            print("cam stop")
            list2.append(0)
            break
        if cv2.waitKey(10) & 0xFF==ord('q'):
            break
        if time.time() - q >= 5:
            print(q)
            print("zaman yenik düştü")
            print("cam stop")
            list2.append(0)
            break
