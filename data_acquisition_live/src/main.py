from threading import Thread,Event
from camera import Camera
import os
import retrain
import label_image



#####Config
##Todo: load config json
output_dir = "./dataz/"
capture_rate = 5 #Hz donut?
classify_rate = 1 #Hz donut?


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

    self.camera = Camera(output_dir,capture_rate=capture_rate)
    self.camera.capture() 

  def get_dir(self,img_n):
    return os.path.join(self.img_dir,self.labels[img_n])

  def capture(self,img_dir):
    self.stop()
    self.camera.set_capture_rate(capture_rate)
    self.camera.set_dir(img_dir)
    self.camera.enable()

  def classify(self):
    self.stop()
    self.batch_train()

    self.classify_dir = os.path.join(self.img_dir,'unclassified')
    if not os.path.exists(self.classify_dir):
      os.mkdir(self.classify_dir)

    self.camera.set_dir(self.classify_dir)
    self.camera.set_capture_rate(classify_rate)
    self.camera.enable(classify=True)
    print 'classifying'

  def batch_train(self):
    retrain.run(self.img_dir)
    print 'batch train: todo'

  def stop(self):
    self.camera.disable()

  def run(self):
    while 1:
      command = raw_input('What is thy bidding?:')
      try:
        self.commands[command]()
      except KeyError:
        print '{} not in commands'.format(command)
  

classifier = Classifier()
classifier.run()



