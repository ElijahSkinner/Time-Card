import gspread
import pandas as pd
from gspread import worksheet
from oauth2client.service_account import ServiceAccountCredentials
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
from datetime import datetime
from time import strftime

################################################################################
# define the scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/Elijah/Downloads/time-card-335501-6f5869e41d19.json',
                                                         scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('Punch Card Systems')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

# get the total number of columns
sheet_instance.col_count

# get the value at the specific cell
sheet_instance.cell(col=3, row=2)


# add a sheet with 20 rows and 2 columns
# sheet.add_worksheet(rows=20,cols=2,title=p1.firstName + p1.lastName)

# get the instance of the second sheet
# currentUserSheet = sheet.get_worksheet(1)


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


# if yesNoQuestion("Do you want to use Punch clock?") == True:
# if p1.clockedIn == True: print("You are already clocked in. "), p1.clockInOut()
# else: print("You are not clocked in. "), p1.clockInOut()


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

        self.listbox = Listbox(self, height=4,
                               width=25,
                               bg="black",
                               activestyle='underline',
                               font="calibri",
                               fg="white")

        self.listbox.insert(1, p1.firstName)
        self.listbox.insert(2, p1.lastName)
        self.listbox.insert(3, p1.email)
        self.listbox.insert(4, p1.payRate)
        self.listbox.pack()

        button1 = Button(self, text="Yes",
                         command=lambda: controller.show_frame("ClockInOutTK"))
        button2 = Button(self, text="Update User Info",
                         command=lambda: controller.show_frame("UpdateInfo"))
        # button1.pack()
        button2.pack()

    def time(self):
        string = strftime('%H:%M:%S %p')
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def clockLabel(self):
        self.clock = Label(self, font=('calibri', 40, 'bold'),
                           background='black',
                           foreground='white')
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
# SPARE PAGE
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
        self.fnLabel = Label(userFrame, text="First Name").grid(row=1)
        self.lnLabel = Label(userFrame, text="Last Name").grid(row=2)
        self.eLabel = Label(userFrame, text="E-mail").grid(row=3)
        self.hwLabel = Label(userFrame, text="Hourly Wage").grid(row=4)

        self.firstN = Entry(userFrame)
        self.lastN = Entry(userFrame)
        self.email = Entry(userFrame)
        self.wage = Entry(userFrame)

        self.listbox = Listbox(userFrame, height=4,
                               width=25,
                               bg="black",
                               activestyle='underline',
                               font="calibri",
                               fg="white")

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
                        command=lambda: [self.updateUserInfo(), self.infoList(), self.clearText()])

        userFrame.grid()  # fix this
        button = Button(self, text="Go Back",
                        command=lambda: controller.show_frame("StartPage"))
        submit.grid(row=6, column=1, sticky=W + E)
        button.grid()

    def infoList(self):
        self.listbox.delete(0, END)
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
# p1.getInfo()
# add a sheet with 20 rows and 2 columns
# sheet.add_worksheet(rows=20,cols=2,title=p1.firstName + " " + p1.lastName)

# sheet_instance.update_value('C2', p1.timeCard)
fullName = (p1.firstName + " " + p1.lastName)
def setWorksheet():
   global currentUserSheet = sheet.worksheet(fullName)

def getUser():
    for r in range(1, sheet_instance.row_count + 1):
        row = sheet_instance.row_values(r)
        if row[0] == fullName:
            print(row[0])
            return True


if getUser():
    setWorksheet()
    print("It WORKS")
    currentUserSheet.update_cell(1, 1, timeStamp())
else:
    sheet.add_worksheet(rows=20, cols=20, title=fullName)
    currentUserSheet.batch_update([{"range" : "B1:S1",
                                   "values" : [["Clock In", "Clock Out", "Clock In", "Clock Out",
                                                "Clock In", "Clock Out", "Clock In", "Clock Out",
                                                "Clock In", "Clock Out", "Clock In", "Clock Out",
                                                "Clock In", "Clock Out", "Clock In", "Clock Out",
                                                "Clock In", "Clock Out"]]},
                                   {"range" : "A1:A20",
                                   "values" : [["Dates", "12/28/21", "12/29/21", "12/30/21", "12/31/21",
                                                "1/1/22", "1/2/22", "1/3/22", "1/4/22", "1/5/22", "1/6/22",
                                                "1/7/22", "1/8/22", "1/9/22", "1/10/22", "1/11/22", "1/12/22",
                                                "1/13/22", "1/14/22", "1/15/22"]]},
                                   ])

    setWorksheet()
     #currentUserSheet.update_cell(1, 1, p1.timeCard)


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
# add a sheet with 20 rows and 2 columns
sheet.add_worksheet(rows=20,cols=2,title=p1.firstName + p1.lastName)



