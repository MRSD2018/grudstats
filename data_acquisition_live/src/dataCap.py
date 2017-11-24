import Tkinter, Tkconstants, tkFileDialog
import cv2
from PIL import Image, ImageTk
import os
import re
import time 
import sys

if sys.platform.startswith('linux'):
    from Tkinter import Tk, Label, Button, Entry, IntVar, Frame, Entry, StringVar, SUNKEN, RAISED, Scale, HORIZONTAL
else:
    from tkinter import Tk, Label, Button, Entry, IntVar, Frame, Entry, StringVar, SUNKEN, RAISED, Scale, HORIZONTAL



########CHANGE THIS UNTIL YOU FIND THE RIGHT CAMERA##############
CameraNum = 0
#######ADD OR REMOVE REQUIRED LABEL CLASSES###################
Labels = ["fairway", "rough", "mixed", "sidewalk", "dirt"]


class DataCollector:

    def __init__(self, master):
        self.master = master
        master.title("Robostats Data Collector")

        global Labels
        self.grassLabels = Labels
        #class vars
        self.isRecording = True
        #self.directory_name = StringVar()
        self.directory_name = "./dataz"
        self.grassLabel = StringVar()
        self.grassLabel.set(self.grassLabels[0])
        self.lastcaptime = 0
        self.count = [IntVar() for i in range(len(self.grassLabels))]
        #self.countText = [StringVar(), StringVar(), StringVar()]
        self.countText = [StringVar() for i in range(len(self.grassLabels))]
        for i in range(len(self.grassLabels)):
        	self.countText[i].set(self.grassLabels[i] + ":" + str(self.count[i].get()))


        self.capRate = 10


        global CameraNum
        self.cap = cv2.VideoCapture(CameraNum)

        self.controlFrame = Frame(self.master)
        self.directory_label = Label(self.controlFrame, text="Save Directory:")
        self.dir_box = Entry(self.controlFrame, width=50, textvariable=self.directory_name)
        self.directoryButton = Button(self.controlFrame, text="Browse", command=self.set_directory)

        self.rateFrame = Frame(self.master)
        self.rateLabel = Label(self.rateFrame, text="Captures per second: ")
        self.rateSlider = Scale(self.rateFrame, from_=.1, to=30, orient=HORIZONTAL, resolution=0.1, sliderlength=15, length=300, command=self.set_rate)


        self.buttonFrame = Frame(self.master)
        self.startButton = Button(self.buttonFrame, text="Start", command=self.start_record, height=5, width=12, bg="#47BD5C")
        self.stopButton = Button(self.buttonFrame, text="Stop", command=self.stop_record, height=5, width=12, bg="red")

        self.labelButtonFrame = Frame(self.master)
        self.typeButton = [Button(self.labelButtonFrame, text=self.grassLabels[i], height=3,command=lambda num=i:self.set_label(num), width=int(50/len(self.grassLabels))) for i in range(len(self.grassLabels))]
        self.typeButton[0].config(relief=SUNKEN, bg="#F7C45D")
        
       
        # self.typeButton = [
        # Button(self.labelButtonFrame, text=self.grassLabels[0], command=lambda:self.set_label(0), height=3, width=10, relief=SUNKEN, bg="#F7C45D"),
        # Button(self.labelButtonFrame, text=self.grassLabels[1], command=lambda:self.set_label(1), height=3, width=10),
        # Button(self.labelButtonFrame, text=self.grassLabels[2], command=lambda:self.set_label(2), height=3, width=10)
        # ]

        self.infoFrame = Frame(self.master)
        self.countLabel = [Label(self.infoFrame, textvariable=self.countText[i]) for i in range(len(self.grassLabels))]
        # self.countLabel = [
        # Label(self.infoFrame, textvariable=self.countText[0]),
        # Label(self.infoFrame, textvariable=self.countText[1]),
        # Label(self.infoFrame, textvariable=self.countText[2])
        # ]



        #layout
        #self.imageFrame.grid(row=0, column=0)
        #self.lmain.grid(row=0, column=0)
        curFrameRow = 0

        self.controlFrame.grid(row=curFrameRow, column=0)
        self.directory_label.grid(row=1, column=0)
        self.dir_box.grid(row=1, column=1)
        self.directoryButton.grid(row=1, column=2)

        curFrameRow+=1

        self.rateFrame.grid(row=curFrameRow, column=0)
        self.rateLabel.grid(row=0, column=0)
        self.rateSlider.grid(row=0, column=1)

        curFrameRow+=1
       
        self.buttonFrame.grid(row=curFrameRow, column=0, pady=10)
        self.startButton.grid(row=0, padx=5)
        self.stopButton.grid(row=0, column=1, padx=5)

        curFrameRow+=1 

        self.labelButtonFrame.grid(row=curFrameRow, column=0)
        col = 0
        for button in self.typeButton:
            button.grid(row=0, column=col, padx = 10)
            col+=1

        curFrameRow +=1

        self.infoFrame.grid(row=curFrameRow, column=0, pady = 10)
        col = 0
        for label in self.countLabel:
            label.grid(row=0, column = col)
            col += 1


    def set_directory(self):
        filename = tkFileDialog.askdirectory()
        self.directory_name.set(filename)
        self.update_counters()

    def set_label(self, num):
    	print "num: " + str(num)
        for i, button in enumerate(self.typeButton):
            if i != num:
                button.config(relief=RAISED, bg=self.master.cget('bg'))
            else:
                button.config(relief=SUNKEN, bg="#F7C45D")
        self.grassLabel.set(self.grassLabels[num])

    def set_rate(self, val):
        self.capRate = float(val)

    def show_frame(self):
        _, frame = self.cap.read()
        #frame = cv2.flip(frame, 1)
        cv2.imshow("Robostats Data Collector", frame)
        cv2.waitKey(1)
        #cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        #img = Image.fromarray(cv2image)
        #imgtk = ImageTk.PhotoImage(image=img)
        #self.lmain.imgtk = imgtk
        #self.lmain.configure(image=imgtk)
        #save if started
        if self.isRecording:
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
              
                    #filename = labelDir + "/" + self.grassLabel.get() + str(maxNum + 1) + ".png"
                    filename = labelDir + "/" + "mylabelz" + str(maxNum + 1) + ".png"
                    #print("saved" + str(filename))
                    cv2.imwrite(filename, frame)

                    self.lastcaptime = millis
                    self.update_counters()

        self.controlFrame.after(10, self.show_frame) 

                
    def start_record(self):
        self.isRecording = True

    def stop_record(self):
        self.isRecording = False
        
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
            #print maxNum
            self.count[i].set(maxNum)

        for i in range(len(self.grassLabels)):
        	self.countText[i].set(self.grassLabels[i] + ":" + str(self.count[i].get()))




root = Tk()
my_gui = DataCollector(root)
my_gui.show_frame()
while 1: 
  my_gui.show_frame()
  time.sleep(1)

#root.mainloop()
