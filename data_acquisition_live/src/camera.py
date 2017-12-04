import cv2
import os
import re
import label_image
from time import time
from threading import Thread,Event,Timer

########CHANGE THIS UNTIL YOU FIND THE RIGHT CAMERA##############
CameraNum = 0

class Camera():
  def __init__(self,img_dir,capture_rate=5):
    self.enabled = False
    self.classify_enabled = False
    global CameraNum
    self.cap = cv2.VideoCapture(CameraNum)
    self.img_dir = img_dir
    self.delay = 1 / float(capture_rate)
    self.set_capture_rate(capture_rate)

  def set_capture_rate(self,capture_rate):
    self.delay = 1 / float(capture_rate)

  def set_dir(self,img_dir):
    self.img_dir = img_dir

  def capture_thread(self):
    last_capture = time()
    #while self.enabled:
    while 1:
      if time() > last_capture + self.delay and self.enabled:
        _, frame = self.cap.read()
        cv2.imshow("Robostats Data Collector", frame)
        cv2.waitKey(1)
        filename = "{}/img_{}.jpg".format(self.img_dir,self.get_img_count()+1)
        cv2.imwrite(filename, frame)
        if self.classify_enabled:
          label_image.label(filename)
        last_capture = time()
    #thread timer, capture just keeps calling itself in perpetuity
    #Timer(self.delay,self.capture).start()

  def capture(self):
    self.capture_thread = Thread(target=self.capture_thread)
    self.capture_thread.daemon = True
    self.capture_thread.start() 

  def get_img_count(self):
    files = []
    for f in [f for f in os.listdir(self.img_dir) if os.path.isfile(os.path.join(self.img_dir,f))]:
      try:
        files.append(int(re.search(r'\d', f).group()))
      except AttributeError:
        pass
    return len(files)

  def enable(self,classify=False):
    self.enabled = True
    self.classify_enabled = classify
  def disable(self):
    self.enabled = False
    self.classify_enabled = False


if __name__ == "__main__":
  c = Camera('data')
  c.capture()
  while 1: pass

