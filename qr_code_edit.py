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
from excel_writer import ExcelWriter
class CameraFeed(Thread):
    input_file_path : str
    output_file_path : str
    def __init__(self):
        super().__init__()
        self.input_file_path = "Sessions.xlsx"
        self.output_file_path = "Main file.xlsx"
        self.excelWriter = ExcelWriter(self.input_file_path, self.output_file_path)
        self.cam = cv.VideoCapture(0)   # change the camera port
        self.oc = owncloud.Client.from_public_link('https://tuc.cloud/index.php/s/areq9npZmFrsara', folder_password = "nnxoP5Y4BR")  # connect to the cloud

    def QR_read(self, image):
        try:
            detect = cv.QRCodeDetector()
            value, points, straight_qrcode = detect.detectAndDecode(image)
            return value, points
        except:
            return None

    def run(self): 
        while(True):
            camera_is_found, image = self.cam.read() # read the camera image
            currentTime = datetime.datetime.now()
            if camera_is_found:
                value, points = self.QR_read(image)

                img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                img = Image.fromarray(img)

                # Calculate the aspect ratio of the image
                aspect_ratio = img.height / img.width
                
                # Calculate the new dimensions
                finalWidth = 350
                finalHeight = int(finalWidth * aspect_ratio)
                
                img = img.resize((finalWidth, finalHeight), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)
                app.imageLabel.config(image = img)
                app.imageLabel.image = img

                app.time.config(text = currentTime.strftime('%d.%m.%Y, %H:%M'))

                if points is None or value == "":   # no QR code detected
                    self.tellNoQRC()
                else:   # QR code detected
                    self.appendQRData(value)
            else:
                self.tellNoCameraFound()

    def tellNoCameraFound(self):
        app.name.config(text = "No Camera Found")   # display message and image if no camera found
        img = (Image.open("no-video.png"))
        img = img.resize((300,300), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        app.imageLabel.config(image = img)
        app.imageLabel.image = img

    def appendQRData(self, value):
        self.downloadRemoteFile(self.output_file_path)
        self.append_to_file(value, self.output_file_path)
        self.upload_to_the_cloud(self.output_file_path)
        time.sleep(3)

    def tellNoQRC(self):
        app.name.config(text = "No QR Code Found")
        app.info.config(text = "")
        app.cloudInfo.config(text = "")
        app.indicator.config(image = '')
        app.indicator.image = ''

    def upload_to_the_cloud(self, file_name):
        try:
            self.oc.drop_file(file_name)  # upload file to cloud
            os.remove(file_name)     # delete local file when upload successful
            app.cloudInfo.config(text = "saved online")
        except:
            app.cloudInfo.config(text = "saved locally")

    def append_to_file(self, value: str, saveFile: str):
        self.excelWriter.append_row_to_excel(saveFile, value, str(datetime.datetime.now()), str(app.selected_entry.get()))
        # TODO: check if the row has been really appended
        app.statusMessage("success")
    
    def downloadRemoteFile(self, saveFile: str):
        self.oc.get_file(saveFile, saveFile) # download remote file

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        
        self.title("QR-Code Scanner")
        #self.attributes('-topmost', 1)         # optionally keep window always in foreground
        #self.attributes('-fullscreen', True)   # optionally set window to fullscreen
       
        self.iconbitmap("qr-code.ico.ico")
                              
        window_width = 1280                     # define window size
        window_height = 500

        screen_width = self.winfo_screenwidth()     # determine screen size
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width/2 - window_width / 2)   # determine the center of the screen
        center_y = int(screen_height/2 - window_height / 2)

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')  # center the window on the screen

        self.columnconfigure(0, weight = 5) # set the size ratio of the different columns
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 5)

        self.camera_thread = CameraFeed()
        self.camera_thread.downloadRemoteFile(self.camera_thread.input_file_path)
        self.camera_thread.daemon = True    # necessary to stop the thread when exiting the program
        self.create_window()        # create the GUI window
        self.camera_thread.start()  # start the camera thread

    def create_window(self):
        standardFont = font.nametofont("TkDefaultFont")

        self.programName = ttk.Label(self, text = "Conference Enrollment", foreground =("white"),background=("#1b7a5a"),padding=(400,20),font = (standardFont, 30),justify=('left')) # program name
        self.name = ttk.Label(self, font = (standardFont, 20))  # display the scanned name
        self.indicator = ttk.Label(self)    # image if enrolment was successful or not
        self.info = ttk.Label(self, text = "", font = (standardFont, 20))   # text if enrolment was successful or not
        self.cloudInfo = ttk.Label(self, text = "", font = (standardFont, 20)) # text for upload status
        self.imageLabel = tk.Label(self, width=200, height=200)   # place for the camera image
        self.time = ttk.Label(self, text = "", font = (standardFont, 20))   # current time
        self.selected_entry = tk.StringVar()
        self.selector = ttk.Combobox(self, textvariable=self.selected_entry, state='readonly')  # session selector
        self.selector['values'] = self.camera_thread.excelWriter.get_sheet_names()  # custom sessions can be entered here
        print(self.selector['values'])
        self.selector.current(0)  # make the first entry the default one
        self.selector.bind("<<ComboboxSelected>>", self.on_combobox_select)
        # Adding a sub OptionMenu
        self.sub_session_var = tk.StringVar()
        self.sub_selector = ttk.OptionMenu(self, self.sub_session_var, *self.camera_thread.excelWriter.get_sessions(self.selector.get()))
        
        # place all GUI elements on the grid layout
        self.programName.grid(column=0, row=0, columnspan=3, padx=15, pady=15, sticky=tk.W)
        self.name.grid(column=2, row=2, sticky=tk.W)
        self.indicator.grid(column=1, row=3, padx=15, pady=15, sticky=tk.E)
        self.info.grid(column=2, row=3, sticky=tk.W)
        self.cloudInfo.grid(column=2, row=4, sticky=tk.W)
        self.imageLabel.grid(column=0, row=1, rowspan=5, padx=15, pady=15)
        self.time.grid(column=2, row=5, padx=15, pady=15, sticky=tk.W)
        self.selector.grid(column=2, row=5, padx=30, pady=15, sticky=tk.E)
        self.sub_selector.grid(column=2, row=6, padx=30, pady=15, sticky=tk.E)
        
    def on_combobox_select(self, event):
        # Get the selected option
        selected_day = self.selector.get()
        print("Selected Option:", selected_day)

        new_options = self.camera_thread.excelWriter.get_sessions(selected_day)
        self.update_option_menu(new_options)
        self.sub_session_var.set(new_options[0])
        
    def update_option_menu(self, options):
        # Access the menu of the OptionMenu widget
        menu = self.sub_selector["menu"]
        menu.delete(0, "end")  # Clear current options
        
        # Add new options to the menu
        for option in options:
            menu.add_command(label=option, command=lambda value=option: self.sub_session_var.set(value))


    def statusMessage(self, status):    # display status message + image
        if status == "file":
            message = "can't write file"
            statusImage = "enrolment_failed.png"
        if status == "success":
            message = "Enrolment was successful"
            statusImage = "enrolment_successful.png"
        self.info.config(text = message)
        newImg = ImageTk.PhotoImage((Image.open(statusImage)).resize((32,32), Image.Resampling.LANCZOS))
        self.indicator.config(image = newImg)
        self.indicator.image = newImg

if __name__ == "__main__":  # lauch the main GUI loop
    app = App()
    app.mainloop()
       
