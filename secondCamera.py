# BETA/v2
import os
import cv2
import numpy as np
import time

class Camera:
    def __init__(self):
        self.state = "off"
        self.rec = False

        self.ID = 1
        self.destination = "C://Users//defaultuser0//PycharmProjects//untitled//"#save file destination

    def getState(self):
        return self.state
    def getID(self):
        return self.ID
    def getDestination(self):
        return self.destination
    def getRec(self):
        return self.rec
    def setState(self,state):
        if type(state) is str:
            if state == "off":#ask to turn off
                if self.state == "on":#turn off camera
                    self.state = "off"
            elif state == "on":
                if self.state == "off":
                    self.state = "on"
                    self.turnIdle()
    def setID(self,id):
        if type(id) is int:
            self.ID = id
    def setDestination(self,des):
        if type(des) is str:
            try:
                if os.path.isdir(des):#if destination exists
                    self.destination = des
            except:
                print("something")
    def setRec(self,b):
        if type(b) is bool:
            self.rec = b

    def turnIdle(self):
        cap = cv2.VideoCapture(self.ID)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        timestr = time.strftime("%Y_%m_%d-%H_%M%S")
        fldr = timestr[:10]
        if os.path.isdir(self.destination+fldr)== False:
            os.makedirs(self.destination+fldr)
        timestr = timestr[11:16]
        out = cv2.VideoWriter(self.destination+fldr+"//"+timestr+'.avi', fourcc, 20.0, (640, 480))
        while self.getState() == "on":
            _,frame = cap.read()

            cv2.imshow('frame', frame)#show capture frame
            #analyze the frame here
            #if found mid-sized difference, start record
            #else close record if open
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                if self.getRec() == False:#turn on rec with esc
                    self.setRec(True)
                else:#turn off, save vid, with esc
                    self.setRec(False)

            elif k == 113 and self.getRec() == False:#if quit with q
                self.setState("off")

            if self.getRec() == True:  # user want to record
                out.write(frame)
        cv2.destroyAllWindows()
        cap.release()
        out.release()  # release recording vid

