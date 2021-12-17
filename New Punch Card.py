from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
from datetime import datetime
from time import strftime
############################################################################################
def timeStamp():
    now = datetime.now()
    current = now.strftime("%m/%d/%y, %H:%M")
    return current


class Employee:
    def __init__(self, firstName, lastName, email, timeCard, payRate):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.timeCard = {}
        self.payRate = 15
        self.clockedIn = False
p1 = Employee("Elijah", "Skinner", "elijah.skinner66@gmail.com", timeStamp(), 15.00)

#if yesNoQuestion("Do you want to use Punch clock?") == True:
   # if p1.clockedIn == True: print("You are already clocked in. "), p1.clockInOut()
    #else: print("You are not clocked in. "), p1.clockInOut()


########################################################################################
class MainApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title('Punch Card Systems')
        self.geometry("500x500")
        self.title_font = tkFont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, ClockInOutTK, UpdateInfo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
    
class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        self.clockLabel()
        self.time()
        clockInButton = Button(self, text="Clock In", command=self.clockIn).pack()
        clockOutButton = Button(self, text="Clock Out", command=self.clockOut).pack()
        
        button1 = Button(self, text="Yes",
                            command=lambda: controller.show_frame("ClockInOutTK"))
        button2 = Button(self, text="Update User Info",
                            command=lambda: controller.show_frame("UpdateInfo"))
        #button1.pack()
        button2.pack()
        
    def time(self):
        string = strftime('%H:%M:%S %p')
        self.clock.config(text = string)
        self.clock.after(1000, self.time)

    def clockLabel(self):
        self.clock = Label(self, font = ('calibri', 40, 'bold'),
                      background = 'black',
                      foreground = 'white')
        self.clock.pack()
        
    def clockIn(self):
        if p1.clockedIn == True:
            messagebox.showwarning('Error', "You are already clocked in!")
        else:
            p1.timeCard["in"] = timeStamp() 
            p1.clockedIn = True

    def clockOut(self):
        if p1.clockedIn == False:
            messagebox.showwarning('Error', "You are already clocked out!")
        else:
            p1.timeCard["out"] = timeStamp()
            p1.clockedIn = False
#################################
        #SPARE PAGE
class ClockInOutTK(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Clock In and Out.", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

       # clockInButton = Button(self, text="Clock In", command=self.clockIn).pack()
       # clockOutButton = Button(self, text="Clock Out", command=self.clockOut).pack()
         
        button = Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
################################
class UpdateInfo(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Update Information", font=controller.title_font)
        label.grid(row=0, columnspan=5)

        userFrame = Frame(self)
        fnLabel = Label(userFrame, text="First Name").grid(row=1)
        lnLabel = Label(userFrame, text="Last Name").grid(row=2)
        eLabel = Label(userFrame, text="E-mail").grid(row=3)
        hwLabel = Label(userFrame, text="Hourly Wage").grid(row=4)

        self.firstN = Entry(userFrame)
        self.lastN = Entry(userFrame)
        self.email = Entry(userFrame)
        self.wage = Entry(userFrame)
        
        self.listbox = Listbox(userFrame, height =4,
                          width = 25,
                          bg = "black",
                          activestyle = 'underline',
                          font = "calibri",
                          fg = "white")
        
        self.listbox.insert(1, p1.firstName)
        self.listbox.insert(2, p1.lastName)
        self.listbox.insert(3, p1.email)
        self.listbox.insert(4, p1.payRate)
        
           
        self.firstN.grid(row=1, column=1)
        self.lastN.grid(row=2, column=1)
        self.email.grid(row=3, column=1)
        self.wage.grid(row=4, column=1)
        self.listbox.grid(row=1, column=3, rowspan=4)

        submit = Button(userFrame, text="Submit",
                        command=lambda:[self.updateUserInfo(), self.infoList(), self.clearText()])
        
        userFrame.grid() #fix this
        button = Button(self, text="Go Back",
                        command=lambda: controller.show_frame("StartPage"))
        submit.grid(row=6, column=1, sticky=W+E)
        button.grid()
        
    def infoList(self):
        self.listbox.delete(0,END) 
        self.listbox.insert(1, p1.firstName)
        self.listbox.insert(2, p1.lastName)
        self.listbox.insert(3, p1.email)
        self.listbox.insert(4, p1.payRate)
            
    def updateUserInfo(self):
        p1.firstName = self.firstN.get()
        p1.lastName = self.lastN.get()
        p1.email = self.email.get()
        p1.payRate = self.wage.get()
        
    def clearText(self):
        self.firstN.delete(0, END) 
        self.lastN.delete(0, END)
        self.email.delete(0, END)
        self.wage.delete(0, END)
        
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
###########################################################################################
#p1.getInfo()




