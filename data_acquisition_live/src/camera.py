import cv2
import os
import re
import label_image
from time import time
from threading import Thread,Event,Timer
from subprocess import Popen, PIPE
import numpy as np


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
    #I got my class. pipe
    self.PIPE_PATH = "/tmp/class_pipe"
    if not os.path.exists(self.PIPE_PATH):
        os.mkfifo(self.PIPE_PATH)
    #Will open a terminal to watch this pipe manually. uncomment to automagically open terminal
    #Popen(['xterm', '-e', 'tail -f %s' % self.PIPE_PATH])

  def set_capture_rate(self,capture_rate):
    self.delay = 1 / float(capture_rate)

  def set_dir(self,img_dir):
    self.img_dir = img_dir

  def capture(self):
    start_time = time()
    delay = self.delay
    if self.enabled:
      _, frame = self.cap.read()
      cv2.imshow("Robostats Data Collector", frame)
      cv2.waitKey(1)
      filename = "{}/img_{}.jpg".format(self.img_dir,self.get_img_count()+1)
      cv2.imwrite(filename, frame)
      #cv2.destroyAllWindows()
      if self.classify_enabled:
        labels,results = label_image.label(filename)
        index_max = np.argmax(results)
        with open(self.PIPE_PATH, "w") as p:
          p.write("{} : {} \n".format(labels[index_max],results[index_max]))
      delay = self.delay - max(0,(time() - start_time))
    #thread timer, capture just keeps calling itself in perpetuity
    Timer(delay,self.capture).start()

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

