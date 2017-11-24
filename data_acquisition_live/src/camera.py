import cv2
import os
import re
#import time 
#import sys
from threading import Thread,Event,Timer

########CHANGE THIS UNTIL YOU FIND THE RIGHT CAMERA##############
CameraNum = 0

#class Camera(Thread):
class Camera():
  #def __init__(self,img_dir,event,capture_rate=5):
  def __init__(self,img_dir,capture_rate=5):
    #Thread.__init__(self)
    #Timer.__init__(self,)
    #self.stopped = event
    self.enabled = False
    global CameraNum
    self.cap = cv2.VideoCapture(CameraNum)
    self.img_dir = img_dir
    self.delay = 1 / float(capture_rate)

  def run(self):
    #while not self.stopped.wait(self.delay) and self.enabled:
    if self.enabled:
      print 'oh hey cameraing'
      self.capture()
      self.start
    Timer(self.delay,self.run).start()

  def enable(self):
    self.enabled = True

  def disable(self):
    self.enabled = False

  def set_dir(self,img_dir):
    self.img_dir = img_dir

  def capture(self):
    if self.enabled:
      _, frame = self.cap.read()
      cv2.imshow("Robostats Data Collector", frame)
      cv2.waitKey(1)
      filename = "{}/img_{}.jpg".format(self.img_dir,self.get_img_count()+1)
      cv2.imwrite(filename, frame)
    Timer(self.delay,self.capture).start()

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
