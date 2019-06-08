import cv2
import xlrd
from xlutils.copy import copy
import time


cam=cv2.VideoCapture(0)
detector=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def addUser(id,name):
    rb = xlrd.open_workbook('users.xls')
    wb = copy(rb)
    sheet = wb.get_sheet(0)
    sheet.write(0,int(id),str(name))
    wb.save('users.xls')


id = input("enter id: ")
name = input("enter name: ")
sampleNum=0

addUser(id,name)
print("Please show all of your face for a good detection...")
while (True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow("faceScreen", img)
        sampleNum = sampleNum + 1
        cv2.imwrite("dataSet/User." + id + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
        print(str(sampleNum) + " tane resim cekildi")
        time.sleep(0.5)
        cv2.imshow('frame', img)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

    elif sampleNum > 20:
        break


cam.release()
cv2.destroyAllWindows()