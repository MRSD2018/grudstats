import cv2
import os
import re
import time 
import sys
from threading import Thread,Event



########CHANGE THIS UNTIL YOU FIND THE RIGHT CAMERA##############
CameraNum = 0
#######ADD OR REMOVE REQUIRED LABEL CLASSES###################
Labels = ["fairway", "rough", "mixed", "sidewalk", "dirt"]


class Camera(Thread):
  def __init__(self,img_dir,event):
    Thread.__init__(self)
    self.stopped = event
    global Labels
    self.grassLabels = Labels
    #self.directory_name = "./dataz"
    self.capRate = 10
    global CameraNum
    self.cap = cv2.VideoCapture(CameraNum)
    self.img_dir = img_dir

  def run(self):
    while not self.stopped.wait(1):
      print self.get_img_count()
      self.capture()
      print("my thread")

  def capture(self):
    _, frame = self.cap.read()
    cv2.imshow("Robostats Data Collector", frame)
    cv2.waitKey(1)
    #if os.path.exists(self.directory_name.get()):
    #if os.path.exists(self.directory_name):
    #labelDir = self.directory_name + "/" + "mylabelz" #self.grassLabel.get()
    #if not os.path.exists(labelDir):
    #  os.makedirs(labelDir)

    #check existing files
    #listOfFiles = [f for f in os.listdir(labelDir)]
    #print listOfFiles
    #maxNum = 0
    #if len(listOfFiles) > 0:
    #  fileNums = [int(re.search(r'\d+', n).group()) for n in listOfFiles]
    #  maxNum = max(fileNums)

    #filename = labelDir + "/" + "mylabelz" + str(maxNum + 1) + ".png"
    filename = "{}/img_{}.jpg".format(self.img_dir,self.get_img_count()+1)
    cv2.imwrite(filename, frame)


  def get_img_count(self):
    files = []
    for f in [f for f in os.listdir(self.img_dir) if os.path.isfile(os.path.join(self.img_dir,f))]:
      try:
        files.append(int(re.search(r'\d', f).group()))
      except AttributeError:
        pass
    return len(files)

if __name__ == "__main__":
  camera = Camera('./dataz',Event())
  print camera.get_img_count()
