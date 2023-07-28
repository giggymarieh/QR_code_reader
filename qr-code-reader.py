import os
from os.path import exists
import tkinter as tk
from tkinter import ttk
from tkinter import font
import cv2 as cv
from PIL import Image,ImageTk
import time
import datetime
from threading import Thread
import owncloud
import pandas as pd

class CameraFeed(Thread):
    def __init__(self):
        super().__init__()
        
        self.cam = cv.VideoCapture(0)   # change the camera port

    def QR_read(self, image):
        try:
            detect = cv.QRCodeDetector()
            value, points, straight_qrcode = detect.detectAndDecode(image)
            return value, points
        except:
            return None

    def modifyFile(self, saveFile, data, value):
        readData = pd.read_excel(saveFile, index_col=None, header=None) # read data from the given excel file
        rows = len(readData.index)  # determine the row count
        with pd.ExcelWriter(saveFile, mode='a', if_sheet_exists="overlay") as writer:   # append one entry to the next empty row
            data.to_excel(writer, header=False, index=False, startrow=rows)
        app.name.config(text = "Welcome " + value)  # display the name from the QR code
        self.statusMessage("success")  

    def statusMessage(self, status):    # display status message + image
        if status == "file":
            message = "can't write file"
            statusImage = "enrolment_failed.png"
        if status == "success":
            message = "Enrolment was successful"
            statusImage = "enrolment_successful.png"
        app.info.config(text = message)
        newImg = ImageTk.PhotoImage((Image.open(statusImage)).resize((32,32), Image.Resampling.LANCZOS))
        app.indicator.config(image = newImg)
        app.indicator.image = newImg

    def run (self):
        while(True):
            result, image = self.cam.read()
            currentTime = datetime.datetime.now()
            if result:
                value, points = self.QR_read(image)

                img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                img = Image.fromarray(img)

                # scale the camera image to always fit in the given space
                finalHeight = 500
                width, height = img.size
                scale = finalHeight / height
                
                img = img.resize((int(width * scale), finalHeight), Image.Resampling.LANCZOS)
                img = img.crop(box = (int(((width * scale) / 2) - (finalHeight / 2)), 0, int(((width * scale) / 2) + (finalHeight / 2)), finalHeight))
                img = ImageTk.PhotoImage(img)
                app.imageLabel.config(image = img)
                app.imageLabel.image = img

                app.time.config(text = currentTime.strftime('%d.%m.%Y, %H:%M'))

                if points is None or value == "":   # no QR code detected
                    app.name.config(text = "No QR Code Found")
                    app.info.config(text = "")
                    app.cloudInfo.config(text = "")
                    app.indicator.config(image = '')
                    app.indicator.image = ''
                else:
                    saveFile = str(app.selected_entry.get()) + ".xlsx"  # get the filename from the selected session entry
                    data = pd.DataFrame([[str(value), str(currentTime)]])   # data format for storing the new entry
                    local_file_exists = exists(saveFile)    # check if a local file exists (only when previously not transmitted to the cloud)
                    cloud_file_exists = False
                    cloud_access = True
                    file_error = False

                    oc = owncloud.Client.from_public_link('https://tuc.cloud/index.php/s/areq9npZmFrsara', folder_password = "nnxoP5Y4BR")  # connect to the cloud
                    try:
                        if oc.file_info(saveFile) != None:  # check if file already exists on the cloud and if cloud access is available
                            cloud_file_exists = True
                    except owncloud.owncloud.HTTPResponseError:
                        cloud_file_exists = False                     
                    except:
                        cloud_access = False
                    
                    if(cloud_file_exists and local_file_exists):
                        try:
                            os.rename(saveFile, "tmp.xlsx") # rename local file
                            oc.get_file(saveFile, saveFile) # download remote file
                            readData = pd.read_excel(saveFile, index_col=None, header=None)
                            rows = len(readData.index)
                            tmpData = pd.read_excel("tmp.xlsx", index_col=None, header=None)    # append contents of local file to downloaded file
                            with pd.ExcelWriter(saveFile, mode='a', if_sheet_exists="overlay") as writer:
                                tmpData.to_excel(writer, header=False, index=False, startrow=rows)
                            self.modifyFile(saveFile, data, value)  # add recently scanned entry to downloaded file
                            os.remove("tmp.xlsx") # delete the old local file
                        except:
                            self.statusMessage("file")
                            file_error = True

                    if(cloud_file_exists and not local_file_exists):
                        oc.get_file(saveFile, saveFile) # download remote file
                        try:
                            self.modifyFile(saveFile, data, value)  # add recently scanned entry to downloaded file
                        except:
                            self.statusMessage("file")
                            file_error = True
                    
                    if(not cloud_file_exists and local_file_exists):
                        try:
                            self.modifyFile(saveFile, data, value)  # add recently scanned entry to local file
                        except:
                            self.statusMessage("file")
                            file_error = True

                    if(not cloud_file_exists and not local_file_exists):
                        try:
                            with pd.ExcelWriter(saveFile, mode='w') as writer:  # create a new file
                                data.to_excel(writer, header=False, index=False, startrow=0)
                            app.name.config(text = "Welcome " + value)
                            self.statusMessage("success")
                        except:
                            self.statusMessage("file")
                            file_error = True
                    
                    if cloud_access and not file_error:
                        try:
                            oc.drop_file(saveFile)  # upload file to cloud
                            os.remove(saveFile)     # delete local file when upload successful
                            app.cloudInfo.config(text = "saved online")
                        except:
                            app.cloudInfo.config(text = "saved locally")           
                    elif not file_error:
                        app.cloudInfo.config(text = "saved locally")            
                                               
                    time.sleep(3)
            else:
                app.name.config(text = "No Camera Found")   # display message and image if no camera found
                img = (Image.open("no-video.png"))
                img = img.resize((300,300), Image.Resampling.LANCZOS)
                img = ImageTk.PhotoImage(img)
                app.imageLabel.config(image = img)
                app.imageLabel.image = img

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("QR-Code Scanner")
        #self.attributes('-topmost', 1)         # optionally keep window always in foreground
        #self.attributes('-fullscreen', True)   # optionally set window to fullscreen
       
        #self.iconbitmap("C:\\Users\\User\\Downloads\\QR_code_reader\\qr_code.ico")
                              
        window_width = 1280                     # define window size
        window_height = 720

        screen_width = self.winfo_screenwidth()     # determine screen size
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width/2 - window_width / 2)   # determine the center of the screen
        center_y = int(screen_height/2 - window_height / 2)

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')  # center the window on the screen

        self.columnconfigure(0, weight = 5) # set the size ratio of the different columns
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 5)

        self.camera_thread = CameraFeed()
        self.camera_thread.daemon = True    # necessary to stop the thread when exiting the program
        self.create_window()        # create the GUI window
        self.camera_thread.start()  # start the camera thread

    def create_window(self):
        standardFont = font.nametofont("TkDefaultFont")

        self.programName = ttk.Label(self, text = "Conference Enrolment", font = (standardFont, 40))
        self.name = ttk.Label(self, font = (standardFont, 20))  # display the scanned name
        self.indicator = ttk.Label(self)    # image if enrolment was successful or not
        self.info = ttk.Label(self, text = "", font = (standardFont, 20))   # text if enrolment was successful or not
        self.cloudInfo = ttk.Label(self, text = "", font = (standardFont, 20)) # text for upload status
        self.imageLabel = ttk.Label(self)   # place for the camera image
        self.time = ttk.Label(self, text = "", font = (standardFont, 20))   # current time
        self.selected_entry = tk.StringVar()
        self.selector = ttk.Combobox(self, textvariable=self.selected_entry, state = 'readonly')    # session selector
        self.selector['values'] = ['session 1', 'session 2', 'session 3']   # custom sessions can be entered here
        self.selector.current(0)    # make the first entry the default one

        # place all GUI elements on the grid layout
        self.programName.grid(column=0, row=0, columnspan=3, padx=15, pady=15)
        self.name.grid(column=2, row=2, sticky=tk.W)
        self.indicator.grid(column=1, row=3, padx=15, pady=15, sticky=tk.E)
        self.info.grid(column=2, row=3, sticky=tk.W)
        self.cloudInfo.grid(column=2, row=4, sticky=tk.W)
        self.imageLabel.grid(column=0, row=1, rowspan=5, padx=15, pady=15)
        self.time.grid(column=2, row=5, padx=15, pady=15, sticky=tk.W)
        self.selector.grid(column=2, row=5, padx=30, pady=15, sticky=tk.E)

if __name__ == "__main__":  # lauch the main GUI loop
    app = App()
    app.mainloop()