from threading import Thread,Event
from camera import DataCollector

stopFlag = Event()
camera = DataCollector(stopFlag)
camera.start()
# this will stop the timer
#stopFlag.set()
#stopFlag.clear()
