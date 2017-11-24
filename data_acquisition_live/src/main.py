from threading import Thread,Event
from camera import Camera
import os

output_dir = "./dataz/"
if not os.path.exists(output_dir):
  os.mkdir(output_dir)


stopFlag = Event()
camera = Camera(output_dir,stopFlag)
camera.start()
# this will stop the timer
#stopFlag.set()
#stopFlag.clear()
