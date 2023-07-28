import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=623
        height=521
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        title=tk.Label(root)
        title["anchor"] = "s"
        ft = tkFont.Font(family='Times',size=28)
        title["font"] = ft
        title["fg"] = "#333333"
        title["justify"] = "center"
        title["text"] = "Attendance registration"
        title.place(x=130,y=20,width=334,height=38)

        start_button=tk.Button(root)
        start_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        start_button["font"] = ft
        start_button["fg"] = "#000000"
        start_button["justify"] = "center"
        start_button["text"] = "Start"
        start_button.place(x=400,y=410,width=70,height=25)
        start_button["command"] = self.start_button_command

        I_agree_checkbox=tk.Checkbutton(root)
        ft = tkFont.Font(family='Times',size=10)
        I_agree_checkbox["font"] = ft
        I_agree_checkbox["fg"] = "#333333"
        I_agree_checkbox["justify"] = "center"
        I_agree_checkbox["text"] = "I agree"
        I_agree_checkbox.place(x=310,y=330,width=70,height=25)
        I_agree_checkbox["offvalue"] = "0"
        I_agree_checkbox["onvalue"] = "1"
        I_agree_checkbox["command"] = self.I_agree_command

        session_listbox=tk.Listbox(root)
        session_listbox["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        session_listbox["font"] = ft
        session_listbox["fg"] = "#333333"
        session_listbox["justify"] = "center"
        session_listbox.place(x=100,y=110,width=80,height=25)

        stop_button=tk.Button(root)
        stop_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        stop_button["font"] = ft
        stop_button["fg"] = "#000000"
        stop_button["justify"] = "center"
        stop_button["text"] = "Stop"
        stop_button.place(x=310,y=410,width=70,height=25)
        stop_button["command"] = self.stop_button_command

    def start_button_command(self):
        print("command")


    def I_agree_command(self):
        print("command")


    def stop_button_command(self):
        print("command")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


# classes and objects
# methods and attributes of classes
# inheritance
# constructor (__init__)
# self
# declaring a method inside a class