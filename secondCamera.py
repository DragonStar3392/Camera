# BETA/v2
import os
import cv2
import numpy as np
import time

class Camera:
    def __init__(self):
        '''There is only 2 state for camera to be in: on/off(makes more sense than T/F)
           Recording status is on or off
           Mode is when it is either user wants to record or leave camera itself to record
           For ID, 1st camera = 0, 2nd = 1, and so on, in this case, laptop camera is 0
           Destination is where user save the recordings/video, preferrably a full path'''
        self.state = "off"
        self.rec = False
        self.mode = "user"

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
    def getMode(self):
        return self.mode
    def turnOff(self):
        self.state = "off"
    def turnOn(self):
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
                print("Sum Ting Wong")
    def recOn(self):
        self.rec = True
    def recOff(self):
        self.rec = False
    def setMode(self,m):
        if type(m) is str:
            if m == "auto":
                self.mode = "auto"
            elif m == "user":
                self.mode = "user"

    def turnIdle(self):
        cap = cv2.VideoCapture(self.ID)

        while self.getState() == "on":
            '''update save file/folder name whether it is user or auto'''
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            timestr = time.strftime("%Y_%m_%d-%H_%M%S")

            '''folder name Y/M/D'''
            fldr = timestr[:10]
            if os.path.isdir(self.destination+fldr)== False:
                os.makedirs(self.destination+fldr)

            '''video name H/M'''
            timestr = timestr[11:16]
            '''output file = destination , fourcc, (set the)fps, videoframe size'''
            out = cv2.VideoWriter(self.destination+fldr+"//"+timestr+'.avi', fourcc, 15.0, (640, 480))

            if self.getMode() == "auto":
                '''Initially, there is no frame to compare to record'''
                previousFrame = None
                diffFrame = None

                '''tNow = current second, fTime = future set second, lock = if recording is on, nothing can be done'''
                tNow = 0
                fTime = 0
                lock = False

                '''while camera is on and is controlled by camera'''
                while self.getMode() == "auto" and self.getState() == "on":
                    _,frame = cap.read()

                    if previousFrame is not None:
                        '''Due to the frames are very similar, if both frames are the same, then the whole frame would be black
                        as rgb(0,0,0) is black'''
                        diffFrame = cv2.subtract(frame,previousFrame)

                        '''We convert the frame to grayscale then apply threshold to convert anything below 60 would be black
                        else would be white(indicate there is/are movement)'''
                        diffgray = cv2.cvtColor(diffFrame, cv2.COLOR_BGR2GRAY)
                        ret, mask = cv2.threshold(diffgray, 60, 255, cv2.THRESH_BINARY)#prev invert

                        #cv2.imshow('mask', mask)#difference between prevFrame and current frame

                        '''get only seconds'''
                        tNow = int(time.strftime("%S"))
                        if tNow == fTime:
                            '''lock from resetting timer and when tNow==fTime, unlock the record lock'''
                            lock = False
                            #print("done unlocking")

                        if cv2.countNonZero(mask) != 0 and self.getRec() == False and lock == False:
                            #print("Colored image/have white color")  # have movement
                            self.recOn()
                            tNow = int(time.strftime("%S"))
                            '''5second record and then recheck if there is movement'''
                            fTime = (tNow + 5) % 60
                            lock = True

                        elif cv2.countNonZero(mask) == 0 and self.getRec() == True and lock == False:
                            '''the moment when no movement is detected'''
                            #print("Image is black")
                            self.recOff()

                    cv2.imshow('frame', frame)  # show capture frame

                    '''save current frame'''
                    previousFrame = frame

                    '''the frame added to the video if recording is on'''
                    if self.getRec() == True:
                        out.write(frame)

                    if self.getState() == "off" and self.getRec() == True:
                        '''Prevents user from closing camera while camera is recording'''
                        print("Cannot turn off while recording.")
                        self.turnOn()

                    if self.getMode() == "user" or self.getState() == "off":
                        '''abrupt change of mode, turn off everything except camera'''
                        if self.getRec() == True:
                            self.recOff()

            elif self.getMode() == "user":
                '''while camera is on and user takes over the camera'''
                while self.getMode() == "user" and self.getState() == "on":
                    _, frame = cap.read()

                    cv2.imshow('frame', frame)  # show capture frame

                    '''the frame added to the video if recording is on'''
                    if self.getRec() == True:
                        out.write(frame)

                    if self.getState() == "off" and self.getRec() == True:
                        '''Prevents user from closing camera while camera is recording'''
                        print("Cannot turn off while recording.")
                        self.turnOn()

                    if self.getMode() == "auto" or self.getState() == "off":
                        '''abrupt change of mode, turn off everything except camera'''
                        if self.getRec() == True:
                            self.recOff()

                    # k = cv2.waitKey(5) & 0xFF
                    # if k == 113 and self.getRec() == False:  # if quit with q
                    #     self.turnOff()

            '''a while loop finished, if still on means that the mode changes, else it is done'''
            cv2.destroyAllWindows()
            cap.release()
            out.release()  # release recording vid

