import Tkinter, Tkconstants, tkFileDialog
import cv2
from PIL import Image, ImageTk
import os
import re
import time 
import sys
from threading import Thread,Event


if sys.platform.startswith('linux'):
    from Tkinter import Tk, Label, Button, Entry, IntVar, Frame, Entry, StringVar, SUNKEN, RAISED, Scale, HORIZONTAL
else:
    from tkinter import Tk, Label, Button, Entry, IntVar, Frame, Entry, StringVar, SUNKEN, RAISED, Scale, HORIZONTAL



########CHANGE THIS UNTIL YOU FIND THE RIGHT CAMERA##############
CameraNum = 0
#######ADD OR REMOVE REQUIRED LABEL CLASSES###################
Labels = ["fairway", "rough", "mixed", "sidewalk", "dirt"]


class DataCollector(Thread):
  def __init__(self,event):
    Thread.__init__(self)
    self.stopped = event
    global Labels
    self.grassLabels = Labels
    self.directory_name = "./dataz"
    self.lastcaptime = 0
    self.capRate = 10
    global CameraNum
    self.cap = cv2.VideoCapture(CameraNum)

  def run(self):
    while not self.stopped.wait(1):
      print("my thread")
      # call a function

  def set_rate(self, val):
    self.capRate = float(val)

  def capture(self):
    _, frame = self.cap.read()
    cv2.imshow("Robostats Data Collector", frame)
    cv2.waitKey(1)
    #if os.path.exists(self.directory_name.get()):
    if os.path.exists(self.directory_name):
      millis = int(round(time.time() * 1000))

      if millis > self.lastcaptime + (1000/self.capRate):
        labelDir = self.directory_name + "/" + "mylabelz" #self.grassLabel.get()
        if not os.path.exists(labelDir):
          os.makedirs(labelDir)

        #check existing files
        listOfFiles = [f for f in os.listdir(labelDir)]
        print listOfFiles
        maxNum = 0
        if len(listOfFiles) > 0:
          fileNums = [int(re.search(r'\d+', n).group()) for n in listOfFiles]
          maxNum = max(fileNums)
  
        filename = labelDir + "/" + "mylabelz" + str(maxNum + 1) + ".png"
        cv2.imwrite(filename, frame)

        self.lastcaptime = millis
        self.update_counters()

     
  def update_counters(self):
    for i, label in enumerate(self.grassLabels):
      labelDir = self.directory_name + "/" + label
      if not os.path.exists(labelDir):
        os.makedirs(labelDir)

      #check existing files
      listOfFiles = [f for f in os.listdir(labelDir)]
      maxNum = 0
      if len(listOfFiles) > 0:
        fileNums = [int(re.search(r'\d+', n).group()) for n in listOfFiles]
        maxNum = max(fileNums)

#my_gui = DataCollector()
#while 1: 
#  my_gui.show_frame()
#  time.sleep(1)


"""
stopFlag = Event()
thread = MyThread(stopFlag)
thread.start()
# this will stop the timer
stopFlag.set()
"""
