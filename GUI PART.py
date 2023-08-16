import tkinter as tk
from tkinter import ttk
from tkinter import font
from threading import Thread
import cv2 as cv


class CameraFeed(Thread):
    def __init__(self):
        super().__init__()
        
        self.cam = cv.VideoCapture(0)   # change the camera port



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("QR-Code Scanner")
        #self.attributes('-topmost', 1)         # optionally keep window always in foreground
        #self.attributes('-fullscreen', True)   # optionally set window to fullscreen
       
        self.iconbitmap("qr-code.ico.ico")
                              
        window_width = 1180                     # define window size
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
        self.camera_thread.daemon = True  # necessary to stop the thread when exiting the program
        self.create_window()        # create the GUI window
        self.camera_thread.start()  # start the camera thread
    
    def create_window(self):
        standardFont = font.nametofont("TkDefaultFont")

        self.programName = ttk.Label(self, text = "Conference Enrollment",foreground =("white"),background=("#1b7a5a"), justify= ("right") ,font = (standardFont, 50))
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


'''
import tkinter as tk
from tkinter import ttk
from tkinter import font
from threading import Thread
import cv2 as cv


class CameraFeed(Thread):
    def __init__(self):
        super().__init__()
        self.cam = cv.VideoCapture(0)   # change the camera port


# Create a custom style for the Combobox
combobox_style = ttk.Style()
combobox_style.layout("Custom.TCombobox",
                      [('Combobox.field',
                        {'children': [('Combobox.downarrow', None),
                                      ('Combobox.padding',
                                       {'children': [('Combobox.textarea',
                                                      {'sticky': 'nswe'})],
                                        'sticky': 'nswe'})],
                         'sticky': 'nswe'})])

combobox_style.configure("Custom.TCombobox", background="#1b7a5a", foreground="#ffffff", borderwidth="3px", justify="center", font=("Times", 12))


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("QR-Code Scanner")
        # self.attributes('-topmost', 1)         # optionally keep window always in foreground
        # self.attributes('-fullscreen', True)   # optionally set window to fullscreen
        self.iconbitmap("qr-code.ico.ico")

        window_width = 1180                     # define window size
        window_height = 720

        screen_width = self.winfo_screenwidth()     # determine screen size
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width/2 - window_width / 2)   # determine the center of the screen
        center_y = int(screen_height/2 - window_height / 2)

        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')  # center the window on the screen

        self.columnconfigure(0, weight=5)  # set the size ratio of the different columns
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=5)

        self.camera_thread = CameraFeed()
        self.camera_thread.daemon = True  # necessary to stop the thread when exiting the program
        self.create_window()        # create the GUI window
        self.camera_thread.start()  # start the camera thread

    def create_window(self):
        standardFont = font.nametofont("TkDefaultFont")

        self.programName = ttk.Label(self, text="Conference Enrollment", foreground="white", background="#1b7a5a", justify="right", font=(standardFont, 50))
        self.name = ttk.Label(self, font=(standardFont, 20))  # display the scanned name
        self.indicator = ttk.Label(self)  # image if enrolment was successful or not
        self.info = ttk.Label(self, text="", font=(standardFont, 20))  # text if enrolment was successful or not
        self.cloudInfo = ttk.Label(self, text="", font=(standardFont, 20))  # text for upload status
        self.imageLabel = ttk.Label(self)  # place for the camera image
        self.time = ttk.Label(self, text="", font=(standardFont, 20))  # current time

        self.selected_entry = tk.StringVar()
        self.selector = ttk.Combobox(self, textvariable=self.selected_entry, state='readonly', style="Custom.TCombobox")
        self.selector['values'] = ['session 1', 'session 2', 'session 3']  # custom sessions can be entered here
        self.selector.current(0)

        # place all GUI elements on the grid layout
        self.programName.grid(column=0, row=0, columnspan=3, padx=15, pady=15)
        self.name.grid(column=2, row=2, sticky=tk.W)
        self.indicator.grid(column=1, row=3, padx=15, pady=15, sticky=tk.E)
        self.info.grid(column=2, row=3, sticky=tk.W)
        self.cloudInfo.grid(column=2, row=4, sticky=tk.W)
        self.imageLabel.grid(column=0, row=1, rowspan=5, padx=15, pady=15)
        self.time.grid(column=2, row=5, padx=15, pady=15, sticky=tk.W)
        self.selector.grid(column=2, row=5, padx=30, pady=15, sticky=tk.E)


if __name__ == "__main__":  # launch the main GUI loop
    app = App()
    app.mainloop()
'''