# -*- coding: utf-8 -*-
#15-112
#Final Project
#Name: Rahaf Khaled
#AndrewID: rabutarb

from Tkinter import *
#First window
class firstWindow:
    def __init__(self):
        self.window=Tk()
        self.bg = PhotoImage(file ="RESIZED.gif")
        self.b1 = PhotoImage(file ="Loginbutton.gif")
        self.b2 = PhotoImage(file ="signup.gif")
        width=self.window.winfo_screenwidth()
        height=self.window.winfo_screenheight() 
        self.window.geometry("%dx%d+0+0"%(width,height))
        self.window.title("Event Planner")
        self.label1=Label(self.window,image=self.bg)
        self.label1.grid()
        self.label2=Label(self.window,text="Don't have an account?",bg="grey",fg="black")
        self.label2.place(x=965,y=500)
        self.loginButton=Button(self.window,image=self.b1,command=self.loginOptions)
        self.loginButton.place(x=865,y=360)
        self.signupButton=Button(self.window,image=self.b2)
        self.signupButton.place(x=870,y=530)
        self.window.mainloop()
    def loginOptions(self):
        self.window.destroy()
        m=optionLogin()

#choose to login as planner or provider
class optionLogin:
    def __init__(self):
        self.window=Tk()
        self.bg = PhotoImage(file ="loginas.gif")
        self.b1 = PhotoImage(file ="plannerbutton.gif")
        self.b2 = PhotoImage(file ="servicebutton.gif")
        width=self.window.winfo_screenwidth()
        height=self.window.winfo_screenheight() 
        self.window.geometry("%dx%d+0+0"%(width,height))
        self.window.title("Event Planner")
        self.label1=Label(self.window,image=self.bg)
        self.label1.grid()
        self.loginButton=Button(self.window,image=self.b1,command=self.plannerButton)
        self.loginButton.place(x=497,y=230)
        self.signupButton=Button(self.window,image=self.b2,command=self.serviceButton)
        self.signupButton.place(x=497,y=530)
        self.window.mainloop()
    def plannerButton(self):
        self.window.destroy()
        m=loginWindowPlanner()
    def serviceButton(self):
        self.window.destroy()
        m=loginWindowService()

#login as planner
class loginWindowPlanner:
    def __init__(self):
        self.window2=Tk()
        self.bg = PhotoImage(file ="loginasplanner.gif")
        width=self.window2.winfo_screenwidth()
        height=self.window2.winfo_screenheight() 
        self.window2.geometry("%dx%d+0+0"%(width,height))
        self.window2.title("Login")
        self.label1=Label(self.window2,image=self.bg)
        self.label1.grid()
        self.loginButton=Button(self.window2,text="Login",command=self.loginButton2)
        self.loginButton.place(x=862,y=458)
        self.loginLabel2=Label(self.window2,text="Username: ",bg='grey', fg='black', width=20,height=2)
        self.loginLabel2.place(x=516,y=265)
        self.userEntry=Entry(self.window2)
        self.userEntry.place(x=716,y=266)
        self.loginLabel2=Label(self.window2,text="Password: ",bg='grey', fg='black', width=20,height=2)
        self.loginLabel2.place(x=516,y=336)
        self.passEntry=Entry(self.window2,show="*")
        self.passEntry.place(x=716,y=336)
        self.window2.mainloop()
    def loginButton2(self):
        self.window2.destroy()
        m=clientDashboard()
        
#login as provider
class loginWindowService:
    def __init__(self):
        self.window3=Tk()
        self.bg = PhotoImage(file ="loginasservice.gif")
        width=self.window3.winfo_screenwidth()
        height=self.window3.winfo_screenheight() 
        self.window3.geometry("%dx%d+0+0"%(width,height))
        self.window3.title("Login")
        self.label1=Label(self.window3,image=self.bg)
        self.label1.grid()
        self.loginButton=Button(self.window3,text="Login")
        self.loginButton.place(x=862,y=458)
        self.loginLabel2=Label(self.window3,text="Username: ",bg='grey', fg='black', width=20,height=2)
        self.loginLabel2.place(x=516,y=265)
        self.userEntry=Entry(self.window3)
        self.userEntry.place(x=716,y=266)
        self.loginLabel2=Label(self.window3,text="Password: ",bg='grey', fg='black', width=20,height=2)
        self.loginLabel2.place(x=516,y=336)
        self.passEntry=Entry(self.window3,show="*")
        self.passEntry.place(x=716,y=336)
        self.window3.mainloop()

#Client's dashboard
class clientDashboard:
    def __init__(self):
        self.window4=Tk()
        self.bg = PhotoImage(file ="dashboard.gif")
        width=self.window4.winfo_screenwidth()
        height=self.window4.winfo_screenheight() 
        self.window4.geometry("%dx%d+0+0"%(width,height))
        self.window4.title("Dashboard")
        self.label1=Label(self.window4,image=self.bg)
        self.label1.grid()
        self.profile = PhotoImage(file ="profile.gif")
        self.profButton=Button(self.window4,image=self.profile)
        self.profButton.place(x=1300,y=100)
        self.eventsLabel=Label(self.window4,text="EVENTS",bg="grey",fg="black")
        self.eventsLabel.place(x=689,y=200)
        self.eventBox=Listbox(self.window4)
        self.eventBox.place(x=630,y=240)
        self.manageButton=Button(self.window4,text="Manage",bg="grey",fg="black",command=self.managing)
        self.manageButton.place(x=600,y=430)
        self.deleteButton=Button(self.window4,text="Delete",bg="grey",fg="black")
        self.deleteButton.place(x=690,y=430)
        self.addButton=Button(self.window4,text="Add Event",bg="grey",fg="black",command=self.add)
        self.addButton.place(x=770,y=430)
        self.window4.mainloop()
        
    def add(self):
        self.window4.destroy()
        m=createEvent()
        
    def managing(self):
        self.window4.destroy()
        m=eventMenu()
    
        

#create new event
class createEvent:
     def __init__(self):
        self.window5=Tk()
        self.bg = PhotoImage(file ="createevent.gif")
        width=self.window5.winfo_screenwidth()
        height=self.window5.winfo_screenheight() 
        self.window5.geometry("%dx%d+0+0"%(width,height))
        self.window5.title("Dashboard")
        self.label1=Label(self.window5,image=self.bg)
        self.label1.grid()
        self.loginLabel2=Label(self.window5,text="Event Name: ",bg='grey', fg='black', width=20,height=2)
        self.loginLabel2.place(x=516,y=265)
        self.userEntry=Entry(self.window5)
        self.userEntry.place(x=716,y=266)
        self.loginLabel2=Label(self.window5,text="Event Type ",bg='grey', fg='black', width=20,height=2)
        self.loginLabel2.place(x=520,y=330)
        #VENUES OPTIONS
        self.venueOptions= [
            "Wedding",
            "Shower",
            "Birthday Party"
        ]
        self.variable = StringVar(self.window5)
        self.variable.set("select a type ") # default value
        self.w = apply(OptionMenu, (self.window5, self.variable) + tuple(self.venueOptions))
        self.w.config(width=20)
        self.w.place(x=720,y=332)
        #ATTENDEES
        self.loginLabel2=Label(self.window5,text="Number of attendees: ",bg='grey', fg='black', width=20,height=2)
        self.loginLabel2.place(x=520,y=400)
        self.numberEntry=Entry(self.window5)
        self.numberEntry.place(x=720,y=410)
        #DATE OF EVENT
        self.dateLabel=Label(self.window5,text="Date of event ",bg='grey', fg='black', width=20,height=2)
        self.dateLabel.place(x=520,y=480)
        #day
        self.days=self.daysOf()
        self.dayVariable=StringVar(self.window5)
        self.dayVariable.set("dd")
        self.daysChoose=apply(OptionMenu,(self.window5,self.dayVariable)+tuple(self.days))
        self.daysChoose.place(x=720,y=480)
        #month
        self.months=self.monthsOf()
        self.monthVariable=StringVar(self.window5)
        self.monthVariable.set("mm")
        self.monthsChoose=apply(OptionMenu,(self.window5,self.monthVariable)+tuple(self.months))
        self.monthsChoose.place(x=810,y=480)
        #year
        self.yearEntry=Entry(self.window5)
        self.yearEntry.place(x=910,y=480)
        #Submit Button
        self.submitButton=Button(self.window5,text="SUBMIT",bg="grey",fg="black",command=self.submitting)
        self.submitButton.place(x=950,y=540)
        self.window5.mainloop()
     def daysOf(self):
         list1=[]
         for i in range(1,32,1):
             list1.append(i)
         return list1
     def monthsOf(self):
         list2=[]
         for i in range(1,13,1):
             list2.append(i)
         return list2
     def submitting(self):
         self.window5.destroy()
         m=eventMenu()

#manage existing event
class eventMenu:
     def __init__(self):
        self.window6=Tk()
        self.bg = PhotoImage(file ="manageevent.gif")
        self.v = PhotoImage(file ="venuebutton.gif")
        self.c = PhotoImage(file ="cateringbutton.gif")
        self.f = PhotoImage(file ="flowersbutton.gif")
        self.g = PhotoImage(file ="guestbutton.gif")
        width=self.window6.winfo_screenwidth()
        height=self.window6.winfo_screenheight() 
        self.window6.geometry("%dx%d+0+0"%(width,height))
        self.window6.title("Event Dashboard")
        self.label1=Label(self.window6,image=self.bg)
        self.label1.grid()
        self.button1=Button(self.window6,image=self.v,command=self.venueSelect)
        self.button1.place(x=330,y=400)
        self.button2=Button(self.window6,image=self.c,command=self.cateringSelect)
        self.button2.place(x=940,y=400)
        self.button3=Button(self.window6,image=self.f)
        self.button3.place(x=330,y=730)
        self.button3=Button(self.window6,image=self.g)
        self.button3.place(x=940,y=730)
        self.window6.mainloop()
     def venueSelect(self):
         self.window6.destroy()
         m=venue()
     def cateringSelect(self):
         self.window6.destroy()
         m=catering()

#venue form         
class venue:
    def __init__(self):
        self.window5=Tk()
        self.bg = PhotoImage(file ="PIC2.gif")
        self.v = PhotoImage(file ="venuebutton.gif")
        width=self.window5.winfo_screenwidth()
        height=self.window5.winfo_screenheight() 
        self.window5.geometry("%dx%d+0+0"%(width,height))
        self.window5.title("Venue")
        self.label1=Label(self.window5,image=self.bg)
        self.label1.grid()
        self.titleLabel=Label(self.window5,image=self.v)
        self.titleLabel.place(x=640,y=70)
        self.selectLabel=Label(self.window5,text="Specify what you need in your venue!")
        self.selectLabel.place(x=400,y=200)
        #venue selection
        self.hotelLabel=Label(self.window5,text="Is there a specific venue?")
        self.hotelLabel.place(x=520,y=272)
        self.venueOptions= [
            "Marriot",
            "W",
            "Intercontinental"
        ]
        self.variable = StringVar(self.window5)
        self.variable.set("select a venue ") # default value
        self.w = apply(OptionMenu, (self.window5, self.variable) + tuple(self.venueOptions))
        self.w.config(width=20)
        self.w.place(x=720,y=272)
        #hotel rating
        self.ratingLabel=Label(self.window5,text="Rating")
        self.ratingLabel.place(x=520,y=372)
        self.ratingOptions= [
            "*",
            "**",
            "***",
            "****",
            "*****"
        ]
        self.variable2 = StringVar(self.window5)
        self.variable2.set("select a rating") # default value
        self.w2 = apply(OptionMenu, (self.window5, self.variable2) + tuple(self.ratingOptions))
        self.w2.config(width=20)
        self.w2.place(x=720,y=372)
        #Budget
        self.budgetLabel=Label(self.window5,text="What is your budget for the venue?")
        self.budgetLabel.place(x=420,y=472)
        self.budgetEntry=Entry(self.window5)
        self.budgetEntry.place(x=720,y=472)
        #submit button
        
        self.window5.mainloop()


#catering form
class catering:
    def __init__(self):
        self.window5=Tk()
        self.bg = PhotoImage(file ="PIC2.gif")
        self.c = PhotoImage(file ="cateringbutton.gif")
        width=self.window5.winfo_screenwidth()
        height=self.window5.winfo_screenheight() 
        self.window5.geometry("%dx%d+0+0"%(width,height))
        self.window5.title("Catering")
        self.label1=Label(self.window5,image=self.bg)
        self.label1.grid()
        self.titleLabel=Label(self.window5,image=self.c)
        self.titleLabel.place(x=640,y=70)
        self.selectLabel=Label(self.window5,text="Specify your catering specifications!")
        self.selectLabel.place(x=400,y=200)
        #venue selection
        self.hotelLabel=Label(self.window5,text="Is there a specific type of cuisine?")
        self.hotelLabel.place(x=420,y=272)
        self.venueOptions= [
            "Mediterranean",
            "Indian",
            "Carribbean",
            "Chinease",
            "Italian",
            "French",
            "Middle Eastern"
            
        ]
        self.variable = StringVar(self.window5)
        self.variable.set("select the type of cuisine ") # default value
        self.w = apply(OptionMenu, (self.window5, self.variable) + tuple(self.venueOptions))
        self.w.config(width=20)
        self.w.place(x=720,y=272)
        #Budget
        self.budgetLabel=Label(self.window5,text="What is your budget for the venue?")
        self.budgetLabel.place(x=420,y=372)
        self.budgetEntry=Entry(self.window5)
        self.budgetEntry.place(x=720,y=372)
        #Allergies
        self.noLabel=Label(self.window5,text="Any allergies or type of food you don't want at your event?")
        self.noLabel.place(x=320,y=472)
        self.noEntry=Entry(self.window5)
        self.noEntry.place(x=720,y=472)
        self.window5.mainloop()
                 
                          
firstWindow()
#####Things that still need to be done with the GUI:
##Signup pages
##Flower+guest list planner
##More Options
##Service providers dashboard
