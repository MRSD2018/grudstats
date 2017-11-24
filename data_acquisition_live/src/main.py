from threading import Thread,Event
from camera import Camera
import os

#####Config
##Todo: load config json
output_dir = "./dataz/"
capture_rate = 5 #Hz donut?
##########


class Classifier():
  def __init__(self):

    self.commands = {'c':self.classify,'s':self.stop}

    self.img_dir = output_dir
    self.labels = []
    n_labels = int(raw_input('How many grudslabels would you like?'))
    for i in range(n_labels):
      label = raw_input('label {}:'.format(i + 1))
      self.labels.append(label)
      label_dir = os.path.join(output_dir,label)
      self.commands[str(i+1)] = lambda d= self.get_dir(i): self.capture(d)
      if not os.path.exists(label_dir):
        os.mkdir(label_dir)

    #self.camera_disable = Event()
    #self.camera_disable.set()
    #self.camera = Camera(output_dir,self.camera_disable,capture_rate=capture_rate)
    self.camera = Camera(output_dir,capture_rate=capture_rate)
    self.camera.capture() 
    #self.camera.start()

  def get_dir(self,img_n):
    return os.path.join(self.img_dir,self.labels[img_n])

  def capture(self,img_dir):
    self.camera.set_dir(img_dir)
    self.camera.enable()
    #self.camera_disable.clear()
    #self.camera.start()

  def classify(self):
    print 'classifying:todo'

  def batch_train(self):
    print 'batch train: todo'

  def stop(self):
    print 'stopping'
    #self.camera_disable.set()
    self.camera_disable.enable()
    #todo:Disable classifier

  def run(self):
    while 1:
      command = raw_input('What is thy bidding?:')
      try:
        self.commands[command]()
      except KeyError:
        print '{} not in commands'.format(command)
  
classifier = Classifier()
classifier.run()
exit()
