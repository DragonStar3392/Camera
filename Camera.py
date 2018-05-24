# ALPHA/v1
# import os
# import cv2
# import numpy as np
#
# class Camera:
#     def __init__(self):
#         self.state = "off"
#         self.ID = 0
#         self.destination = "C:/"#save file destination
#         self.cap = cv2.VideoCapture(self.ID)
#         self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
#         self.out = cv2.VideoWriter('output.avi',self.fourcc,20.0,(640,480))
#         self.frame = None
#     def getState(self):
#         return self.state
#     def getID(self):
#         return self.ID
#     def getDestination(self):
#         return self.destination
#     def setState(self,state):
#         if type(state) is str:
#             if state == "off":#ask to turn off
#                 if self.state == "record":#cannot turn off when recording
#                     return print("cannot turn off when recording")
#                 elif self.state == "idle":#turn off camera
#                     self.state = "off"
#                     self.turnOff()
#             elif state == "idle":
#                 if self.state == "off":
#                     self.turnIdle()
#                     self.state = "idle"
#                 elif self.state == "record": #from record to idle
#                     self.turnIdle()
#                     self.state = "idle"
#             elif state == "record":
#                 if self.state == "idle":
#                     self.state = "record"
#                     self.turnRecord()
#     def setID(self,id):
#         if type(id) is int:
#             self.ID = id
#     def setDestination(self,des):
#         if type(des) is str:
#             try:
#                 if os.path.isdir(des):#if destination exists
#                     self.destination = des
#             except:
#                 print("something")
#     def turnOff(self):
#         self.cap.release()
#         self.cap.destroyAllWindows()
#
#     def turnIdle(self):
#         if self.state is "off":
#             while True:
#                 ret,self.frame = self.cap.read()
#                 cv2.imshow('frame',self.frame)
#
#
#         elif self.state is "record":
#             self.out.release()  # release recording vid
#
#     def turnRecord(self):
#         self.out.write(self.frame)
#
