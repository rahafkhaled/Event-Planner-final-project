# -*- coding: utf-8 -*-
#15-112
#Final Project
#Name: Rahaf Khaled
#AndrewID: rabutarb
import socket
from Tkinter import *
import tkMessageBox
import ScrolledText
import time
#chat client helper functions
def lengthOfMessage(message):
    if len(str(len(message)))==2:
        return "0"+str(len(message))
    elif len(str(len(message)))==1:
        return "00"+str(len(message))
    else:
        return str(len(message))
def lengthOfSize(size):
    if len(size)==1:
        return "0000"+str(size)
    elif len(size)==2:
        return "000"+str(size)
    elif len(size)==3:
        return "00"+str(size)
    elif len(size)==4:
        return "0"+str(size)
    else:
        return str(size)
  
def leftrotate (x, c):
      return (x << c)&0xFFFFFFFF | (x >> (32-c)&0x7FFFFFFF>>(32-c))    

def openFiles(FileName):
    f=open(FileName,"r")
    fileContent=""
    line=f.readline()
    while line:
        fileContent+=line
        line=f.readline()
    f.close()
    return fileContent

########## START OF CHAT CLIENT CODE ##########
def StartConnection (IPAddress, PortNumber):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IPAddress, PortNumber))
    return s

def login (s, username, password):
    #message digest
    s.send("LOGIN "+ username +" \n")
    answer=s.recv(512)
    usernameIndex=answer.find(username)
    PD=password
    CH=answer[(usernameIndex+len(username)+1):].strip()
    n=len(PD)
    m=len(CH)
    message=PD+CH
    numberOfZeros=(512-len(message)-4)
    zeros=["0"]*numberOfZeros
    block=message+"1"+str("".join(zeros))+lengthOfMessage(message)
    M=[]
    chunks=[block[i:i+32] for i in range(0, len(block), 32)]
    sumOfAscii=0
    for i in chunks:
        for m in i:
            ascii=ord(m)
            sumOfAscii+=ascii
        M.append(sumOfAscii)
        sumOfAscii=0
                
    S=[7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,5, 9, 14, 20, 5, 9, 14, 20, 5, 9,
         14,20, 5, 9, 14, 20,4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16,23,6, 10, 15, 21,
         6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21 ]
    K=[0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee ,0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501 ,0x698098d8,
         0x8b44f7af, 0xffff5bb1, 0x895cd7be ,0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821 ,0xf61e2562,
         0xc040b340, 0x265e5a51, 0xe9b6c7aa,0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8, 0x21e1cde6,
         0xc33707d6, 0xf4d50d87, 0x455a14ed,0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 0xfffa3942,
         0x8771f681, 0x6d9d6122, 0xfde5380c ,0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70 ,0x289b7ec6,
         0xeaa127fa, 0xd4ef3085, 0x04881d05 ,0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665 ,0xf4292244,
         0x432aff97, 0xab9423a7, 0xfc93a039 ,0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1 , 0x6fa87e4f,
         0xfe2ce6e0, 0xa3014314, 0x4e0811a1 ,0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391 ]
    #Initialize variables:
    a0=0x67452301   #A
    b0=0xefcdab89   #B
    c0=0x98badcfe   #C
    d0=0x10325476   #D
    A=a0
    B=b0
    C=c0
    D=d0
    #Main loop:
    for i in range(64):
        if 0 <= i <= 15: 
            F=(B & C) | ((~ B) & D)
            F=F & 0xFFFFFFFF
            g=i
        elif 16 <= i<= 31:
            F=(D & B) | ((~ D) & C)
            F=F & 0xFFFFFFFF
            g=(5*i + 1) % 16
        elif 32 <= i <= 47:
            F=B ^ C ^ D
            F=F & 0xFFFFFFFF
            g=(3*i + 5) % 16
        elif 48 <= i <= 63:
            F=C ^ (B | (~ D))
            F=F & 0xFFFFFFFF
            g=(7*i) % 16
        dTemp=D
        D=C
        C=B
        B=B + leftrotate((A + F + K[i] + M[g]), S[i])
        B=B & 0xFFFFFFFF
        A=dTemp
      
  #Add this chunk's hash to result so far:
    a0=(a0 + A) & 0xFFFFFFFF
    b0=(b0 + B) & 0xFFFFFFFF
    c0=(c0 + C) & 0xFFFFFFFF
    d0=(d0 + D) & 0xFFFFFFFF
    result=str(a0)+str(b0)+str(c0)+str(d0)
    s.send("LOGIN "+username+" "+result+" "+" \n")
    data = s.recv(512)
    if "Successful" in data:
        return True
    else:
        return False

        
def sendFriendRequest(s, friend):
    #finds the size and converts it to a string
    size=str(6+len("@request@friend")+1+len(friend))
    size2=lengthOfSize(size)
    s.send("@"+size2+"@request@friend"+"@"+friend)
    answer=s.recv(512)
    if "ok" in answer: 
        return True
    else:
        return False
  

def acceptFriendRequest(s, friend):
    #finds the size and converts it to a string
    size=str(6+len("@accept@friend")+1+len(friend))
    size2=lengthOfSize(size)
    s.send("@"+size2+"@accept@friend"+"@"+friend)
    answer=s.recv(512)
    if "@ok" in answer:
        return True
    else:
        return False
    
def sendMessage(s, friend, message):
    #finds the size and converts it to a string
    size=str(6+len("@sendmsg")+1+len(friend)+1+len(message))
    size2=lengthOfSize(size)
    s.send("@"+size2+"@sendmsg@"+friend+"@"+message)
    print len("@"+size2+"@sendmsg@"+friend+"@"+message), size2
    answer=s.recv(512)
    print "this", answer
    if  "@ok" in answer:
        return True
    else:
        return False

def sendFile(s, friend, filename):
    files= openFiles(filename)
    size=str(6+len("@sendfile")+1+len(friend)+1+len(filename)+1+len(files))
    size2=lengthOfSize(size)
    s.send("@"+size2+"@sendfile"+"@"+friend+"@"+filename+"@"+files)
    answer=s.recv(512)
    if "@ok" in answer:
        return True
    else:
        return False
    


def getMail(s):
    s.send("@rxmsg\n")
    answer=s.recv(512)
    userIndex=6
    #returns the answer starting the number of friends
    number=answer[userIndex+1:]
    #finds first @ after number
    findFirstUser=number.find("@")
    Users=number[findFirstUser+1:]
    listUsers=Users.split("@")
    messageList=[]
    fileList=[]
    for i in range(len(listUsers)):
        if listUsers[i]=="msg":
            messageList.append((listUsers[i+1],listUsers[i+2]))
        if listUsers[i]=="file":
            fileList.append((listUsers[i+1],listUsers[i+2]))
            f=open(listUsers[i+2],"w")
            f.write(listUsers[i+3])
            f.close()           
    #checks if there are 0 users
    if findFirstUser==-1:
       return ([],[])
    else:
        return (messageList,fileList)
   

########## END OF CHAT CLIENT CODE ##########
########## START OF GUI ##########
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
        self.signupButton=Button(self.window,image=self.b2,command=self.signupOptions)
        self.signupButton.place(x=870,y=530)
        self.window.mainloop()
    def loginOptions(self):
        self.window.destroy()
        m=optionLogin()
    def signupOptions(self):
        self.window.destroy()
        m=signupOption()

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
        self.backButton=Button(self.window,text="Go Back",command=self.backButton2)
        self.backButton.place(x=80,y=100)
        self.window.mainloop()
    def plannerButton(self):
        self.window.destroy()
        m=loginWindowPlanner()
    def serviceButton(self):
        self.window.destroy()
        m=loginWindowService()
    def backButton2(self):
        self.window.destroy()
        m=firstWindow()

       
allMessages=[]
#login as planner
class loginWindowPlanner:
    def __init__(self):
        self.connection=StartConnection("86.36.46.10", 15112)
        login (self.connection, "rabutarb2", "rabutarb")
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
        self.backButton=Button(self.window2,text="Go Back",command=self.backButton2)
        self.backButton.place(x=80,y=100)
        self.window2.mainloop()
        
    def loginButton2(self):
        message=""
        s=self.connection
        username=self.userEntry.get()
        password=self.passEntry.get()
        sendMessage(self.connection,"rabutarb1","loginplanner:usr:"+username+":passwrd:"+password+"\n")
        allMessages = getMail(s)
        print allMessages
        allMessages=allMessages[0]
        if allMessages!=[]:
            for i in allMessages:
                message=i[1]
        if message=="Yes":
            f=open("username.txt","w")
            actualUser=self.userEntry.get()
            f.write(actualUser)
            f.close()
            self.window2.destroy()
            m=clientDashboard()
        else:
            tkMessageBox.showinfo("Error", "Username or Password incorrect.")
    def backButton2(self):
        self.window2.destroy()
        m=optionLogin()
            
#login as provider
class loginWindowService:
    def __init__(self):
        self.connection=StartConnection("86.36.46.10", 15112)
        login (self.connection, "rabutarb2", "rabutarb")
        self.window2=Tk()
        self.bg = PhotoImage(file ="loginasservice.gif")
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
        self.backButton=Button(self.window2,text="Go Back",command=self.backButton2)
        self.backButton.place(x=80,y=100)
        self.window2.mainloop()
        
    def loginButton2(self):
        message=""
        s=self.connection
        username=self.userEntry.get()
        f=open("temp2.txt","w")
        f.write(username)
        f.close()
        password=self.passEntry.get()
        sendMessage(self.connection,"rabutarb1","loginservice:usr:"+username+":passwrd:"+password+"\n")
        allMessages = getMail(s)
        allMessages=allMessages[0]
        if allMessages!=[]:
            for i in allMessages:
                message=i[1]
        if message=="Yes":
            self.window2.destroy()
            m=serviceDashboard()
        else:
            tkMessageBox.showinfo("Error", "Username or Password incorrect.")
    def backButton2(self):
        self.window2.destroy()
        m=optionLogin()
            


#Signup option
class signupOption:
    def __init__(self):
        self.window3=Tk()
        self.bg = PhotoImage(file ="signup2.gif")
        self.o1 = PhotoImage(file ="plannerbutton.gif")
        self.o2 = PhotoImage(file ="servicebutton.gif")
        width=self.window3.winfo_screenwidth()
        height=self.window3.winfo_screenheight() 
        self.window3.geometry("%dx%d+0+0"%(width,height))
        self.window3.title("Sign up")
        self.label1=Label(self.window3,image=self.bg)
        self.label1.grid()
        self.planner1Button=Button(self.window3,image=self.o1,command=self.plannerButton)
        self.planner1Button.place(x=497,y=230)
        self.backButton=Button(self.window3,text="Go Back",command=self.backButton2)
        self.backButton.place(x=80,y=100)
        self.window3.mainloop()
    def plannerButton(self):
        self.window3.destroy()
        m=plannerSignup()

    def backButton2(self):
          self.window3.destroy()
          m=firstWindow()


class plannerSignup:
    def __init__(self):
        self.connection=StartConnection("86.36.46.10", 15112)
        login (self.connection, "rabutarb2", "rabutarb")
        self.window2=Tk()
        self.bg = PhotoImage(file ="plannersignup.gif")
        width=self.window2.winfo_screenwidth()
        height=self.window2.winfo_screenheight() 
        self.window2.geometry("%dx%d+0+0"%(width,height))
        self.window2.title("Sign Up")
        self.label1=Label(self.window2,image=self.bg)
        self.label1.grid()
        self.signupButton=Button(self.window2,text="Sign Up",command=self.signupButton2)
        self.signupButton.place(x=862,y=458)
        self.signupLabel2=Label(self.window2,text="Username: ",bg='grey', fg='black', width=20,height=2)
        self.signupLabel2.place(x=516,y=265)
        self.userEntry=Entry(self.window2)
        self.userEntry.place(x=716,y=266)
        self.signupLabel2=Label(self.window2,text="Password: ",bg='grey', fg='black', width=20,height=2)
        self.signupLabel2.place(x=516,y=336)
        self.passEntry=Entry(self.window2,show="*")
        self.passEntry.place(x=716,y=336)
        self.backButton=Button(self.window2,text="Go Back",command=self.backButton2)
        self.backButton.place(x=80,y=100)
        self.window2.mainloop()

    def signupButton2(self):
        s=self.connection
        username=self.userEntry.get()
        password=self.passEntry.get()
        sendMessage(self.connection,"rabutarb1","signupplanner:usr:"+username+":passwrd:"+password+"\n")
        allMessages = getMail(s)
        allMessages=allMessages[0]
        if allMessages!=[]:
            for i in allMessages:
                message=i[1]
            if message=="ok":
                self.window2.destroy()
                m=clientDashboard()
            else:
                tkMessageBox.showinfo("Error", "Username already exists.")
                
    def backButton2(self):
          self.window2.destroy()
          m=signupOption()
          

 

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
    
        
#Service Providers Dashboard
class serviceDashboard:
    def __init__(self):
        self.window4=Tk()
        self.bg = PhotoImage(file ="dashboard.gif")
        width=self.window4.winfo_screenwidth()
        height=self.window4.winfo_screenheight() 
        self.window4.geometry("%dx%d+0+0"%(width,height))
        self.window4.title("Dashboard")
        self.label1=Label(self.window4,image=self.bg)
        self.label1.grid()
        self.mail = PhotoImage(file ="mail.gif")
        self.mailButton=Button(self.window4,image=self.mail,command=self.mailButton2)
        self.mailButton.place(x=600,y=300)
        self.window4.mainloop()
    def mailButton2(self):
        self.window4.destroy()
        m=chatWithClient()

#View latest message
class chatWithClient:
    def __init__(self):
        self.connection=StartConnection("86.36.46.10", 15112)
        login (self.connection, "rabutarb3", "rabutarb")
        self.window5=Tk()
        self.bg = PhotoImage(file ="PIC2.gif")
        width=self.window5.winfo_screenwidth()
        height=self.window5.winfo_screenheight() 
        self.window5.geometry("%dx%d+0+0"%(width,height))
        self.window5.title("Chat with your client")
        self.label1=Label(self.window5,image=self.bg)
        self.label1.grid()
        self.display=ScrolledText.ScrolledText(self.window5,width=80)
        self.display.place(x=400,y=300)
        #recieving
        message=""
        allMessages = getMail(self.connection)
        allMessages=allMessages[0]
        if allMessages!=[]:
            for i in allMessages:
                message=i[1]
        f=open("temp2.txt","r")
        hotel2=f.read()
        f.close()
        mList=message.split("-")
        
        if mList[0].lower()==hotel2.lower():
            self.display.insert(END,"User:"+mList[1]+"\n")
            self.display.insert(END,"Type of event:"+mList[2]+"\n")
            self.display.insert(END,"Date:"+mList[3]+"\n")
            self.display.insert(END,"Time:"+mList[4]+"\n")
            self.display.insert(END,"Capacity:"+mList[5]+"\n")
        else:
            self.display.insert(END,"No Requests")
        #Your messages
        self.messageEntry=Entry(self.window5,width=40)
        self.messageEntry.place(x=470,y=470)
        self.backButton=Button(self.window5,text="Go Back",command=self.backButton2)
        self.backButton.place(x=80,y=100)
        self.window5.mainloop()
    def backButton2(self):
        self.window5.destroy()
        m=serviceDashboard()
        

       
#create new event
class createEvent:
     def __init__(self):
        self.window5=Tk()
        self.info = []
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
        self.backButton=Button(self.window5,text="Go Back",command=self.backButton2)
        self.backButton.place(x=80,y=100)
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
        #Time of event
        self.timeLabel=Label(self.window5,text= "Time of Event")
        self.timeLabel.place(x=520,y=560)
        self.timeEntryBox1=Entry(self.window5,width=2)
        self.timeEntryBox1.place(x=700,y=560)
        self.colonLabel=Label(self.window5,text=":",width=2)
        self.colonLabel.place(x=740,y=562)
        self.timeEntryBox2=Entry(self.window5,width=2)
        self.timeEntryBox2.place(x=780,y=560)
        self.ampmVariable=StringVar(self.window5)
        self.ampmVariable.set("am/pm")
        self.ampmOptions=[
            "am",
            "pm"
            ]
        self.ampmChoose=apply(OptionMenu,(self.window5,self.ampmVariable)+tuple(self.ampmOptions))
        self.ampmChoose.place(x=820,y=560)
        #Submit Button
        self.submitButton=Button(self.window5,text="SUBMIT",bg="grey",fg="black",command=self.submitting)
        self.submitButton.place(x=950,y=600)
        self.backButton=Button(self.window5,text="Go Back",command=self.backButton2)
        self.backButton.place(x=80,y=100)
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
     def tempFolder(self):
         self.info=[]
         typeOfEvent=self.variable.get()+"\n"
         self.info.append(typeOfEvent)
         capacity=self.numberEntry.get()+"\n"
         self.info.append(capacity)
         date=self.dayVariable.get()+"/"+self.monthVariable.get()+"/"+self.yearEntry.get()+"\n"
         self.info.append(date)
         time=self.timeEntryBox1.get()+"."+self.timeEntryBox2.get()+"\n"
         self.info.append(time)
         f=open("temp.txt","w")
         f.writelines(self.info)
         f.close()
     def submitting(self):
         self.tempFolder()
         self.window5.destroy()
         m=eventMenu()
     def backButton2(self):
         self.window5.destroy()
         m=clientDashboard()



#manage existing event
class eventMenu:
     def __init__(self):
        self.window6=Tk()
        self.bg = PhotoImage(file ="manage2.gif")
        self.v = PhotoImage(file ="venuebutton.gif")
        self.c = PhotoImage(file ="cateringbutton.gif")
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
        self.button3=Button(self.window6,image=self.g,command=self.guestSelect)
        self.button3.place(x=625,y=730)
        self.backButton=Button(self.window6,text="Go Back",command=self.backButton2)
        self.backButton.place(x=80,y=100)
        self.window6.mainloop()
     def venueSelect(self):
         self.window6.destroy()
         m=venue()
     def cateringSelect(self):
         self.window6.destroy()
         m=catering()
     def guestSelect(self):
         self.window6.destroy()
         m=guestList()
     def backButton2(self):
         self.window6.destroy()
         m=createEvent()



#guest list
class guestList:
    def __init__(self):
        self.window4=Tk()
        self.bg = PhotoImage(file ="PIC2.gif")
        width=self.window4.winfo_screenwidth()
        height=self.window4.winfo_screenheight() 
        self.window4.geometry("%dx%d+0+0"%(width,height))
        self.window4.title("Dashboard")
        self.label1=Label(self.window4,image=self.bg)
        self.label1.grid()
        self.display=ScrolledText.ScrolledText(self.window4,width=150)
        self.display.place(x=140,y=50)
        self.guestEntry=Entry(self.window4,width=20)
        self.guestEntry.place(x=150,y=450)
        self.send=Button(self.window4,text="Add",command=self.sendButton)
        self.send.place(x=350,y=450)
        f=open("temp.txt","r")
        info2=f.readlines()
        guests=info2[1]
        f.close()
        self.backButton=Button(self.window4,text="Go Back",command=self.backButton2)
        self.backButton.place(x=80,y=100)
        self.window4.mainloop()
        
    def sendButton(self):
        self.display.insert(END,self.guestEntry.get()+"\n")
        self.messageEntry.delete(0,END)
    def backButton2(self):
        self.window4.destroy()
        m=eventMenu()
        
#venue form
class venue:
    def __init__(self):#capacity
        self.connection=StartConnection("86.36.46.10", 15112)
        login (self.connection, "rabutarb2", "rabutarb")
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
        self.hotelLabel=Label(self.window5,text="What type of hall would you like?")
        self.hotelLabel.place(x=420,y=272)
        self.venueOptions= [
            "Ballroom",
            "Reception",
            "Banquet ",
            "Pool View",
            "Garden"
        ]
        self.variable = StringVar(self.window5)
        self.variable.set("select a venue") # default value
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
        #Location
        self.locationLabel=Label(self.window5,text="Select your location -in Qatar-")
        self.locationLabel.place(x=420,y=472)
        self.locationOptions=[
            "Airport street",
            "Al luqta",
            "Corniche",
            "The pearl"
            ]
        self.variable3= StringVar(self.window5)
        self.variable3.set("select a location") #default value
        self.w3= apply(OptionMenu, (self.window5, self.variable3) + tuple(self.locationOptions))
        self.w3.config(width=20)
        self.w3.place(x=720,y=472)

        #Budget
        self.budgetLabel=Label(self.window5,text="What is your budget for the venue?")
        self.budgetLabel.place(x=420,y=572)
        self.budgetEntry=Entry(self.window5)
        self.budgetEntry.place(x=720,y=572)
        #submit button
        submitButton=Button(self.window5,text="Submit",command=self.submitButton2)
        submitButton.place(x=920,y=672)
        self.backButton=Button(self.window5,text="Go Back",command=self.backButton2)
        self.backButton.place(x=80,y=100)
        #hotels results
        self.window5.mainloop()
        
    def backButton2(self):
        self.window5.destroy()
        m=eventMenu()
    def submitButton2(self):
        message=""
        typesM=""
        ratingM=""
        locationM=""
        capacityM=""
        budgetM=""
        s=self.connection
        hallType=self.variable.get()
        ratingOfHotel=self.variable2.get()
        locationOfHotel=self.variable3.get()
        budget=self.budgetEntry.get()
        f=open("temp.txt","r")
        info2=f.readlines()
        guests=info2[1]
        f.close()
        sendMessage(self.connection,"rabutarb1","venue:type:"+hallType+":rating:"+ratingOfHotel+":location:"+locationOfHotel+":budget:"+budget+":capacity:"+guests+"\n")
        allMessages = getMail(s)
        allMessages=allMessages[0]
        if allMessages!=[]:
            for i in allMessages:
                message=i[1]
                if "Types" in message:
                    colonIndex=message.find(":")
                    typesM=message[colonIndex+1:]
                if "Rating" in message:
                    colonIndex=message.find(":")
                    ratingM=message[colonIndex+1:]
                if "Location" in message:
                    colonIndex=message.find(":")
                    locationM=message[colonIndex+1:]
                if "Capacity" in message:
                    colonIndex=message.find(":")
                    capacityM=message[colonIndex+1:]
                if "Budget" in message:
                    colonIndex=message.find(":")
                    budgetM=message[colonIndex+1:]
            m=hotelWindow(ratingM,locationM,typesM,capacityM,budgetM)
            return m

      
                    

  
     
#What you got as a result from your form and pick a venue
class hotelWindow:
    def __init__(self,rating,location,types,capacity,price):
        self.connection=StartConnection("86.36.46.10", 15112)
        login (self.connection, "rabutarb2", "rabutarb")
        self.window5=Toplevel()
        self.bg = PhotoImage(file ="makechoice.gif")
        self.width=self.window5.winfo_screenwidth()
        self.height=self.window5.winfo_screenheight() 
        self.window5.geometry("%dx%d+0+0"%(self.width,self.height))
        self.window5.title("Venue")
        self.label1=Label(self.window5,image=self.bg)
        self.label1.grid()
        #boxes
        #values
        self.rating=rating.split("-")
        self.location=location.split("-")
        self.types=types.split("-")
        self.capacity=capacity.split("-")
        self.budget=price.split("-")
        #rating
        ratingLabel=Label(self.window5,text="Rating")
        ratingLabel.place(x=260,y=180)
        ratingButton=Button(self.window5,text="Select",command=self.ratingButton2)
        ratingButton.place(x=260,y=380)
        self.ratingBox=Listbox(self.window5)
        self.ratingBox.place(x=200,y=200)
        if self.rating==[ ]:
            self.ratingBox.insert(END,"No results for this rating")
        else:
            for r in range(len(self.rating)):
                self.ratingBox.insert(END,self.rating[r])
        #location
        locationLabel=Label(self.window5,text="Location")
        locationLabel.place(x=660,y=180)
        locationButton=Button(self.window5,text="Select",command=self.locationButton2)
        locationButton.place(x=660,y=380)
        self.locationBox=Listbox(self.window5)
        self.locationBox.place(x=600,y=200)
        if self.location==[]:
            self.locationBox.insert(END,"No results for this location")
        else:
            for r in range(len(self.location)):
                self.locationBox.insert(END,self.location[r])
        #Type
        typeLabel=Label(self.window5,text="Type")
        typeLabel.place(x=1060,y=180)
        typeButton=Button(self.window5,text="Select",command=self.typeButton2)
        typeButton.place(x=1060,y=380)        
        self.typeBox=Listbox(self.window5)
        self.typeBox.place(x=1000,y=200)
        if self.types==[]:
            self.typeBox.insert(END,"No results for this type of hall")
        else:
            for r in range(len(self.types)):
                self.typeBox.insert(END,self.types[r])
        #capacity
        capacityLabel=Label(self.window5,text="Capacity")
        capacityLabel.place(x=460,y=380)
        capacityButton=Button(self.window5,text="Select",command=self.capacityButton2)
        capacityButton.place(x=460,y=580)
        self.capacityBox=Listbox(self.window5)
        self.capacityBox.place(x=400,y=400)
        if self.capacity==[]:
            self.capacityBox.insert(END,"No results for this capacity")
        else:
            for r in range(len(self.capacity)):
                self.capacityBox.insert(END,self.capacity[r])
        #Budget
        budgetLabel=Label(self.window5,text="Budget")
        budgetLabel.place(x=860,y=380)
        budgetButton=Button(self.window5,text="Select",command=self.budgetButton2)
        budgetButton.place(x=860,y=580)
        self.budgetBox=Listbox(self.window5)
        self.budgetBox.place(x=800,y=400)
        if self.budget==[]:
            self.budgetBox.insert(END,"No results for this Budget")
        else:
            for r in range(len(self.budget)):
                self.budgetBox.insert(END,self.budget[r])
        self.window5.mainloop()
        #rating button
    def gettingInfo(self):
            info=[]
            f=open("temp.txt","r")
            info=f.readlines()
            f.close()
            y=open("username.txt","r")
            info2=y.readline()
            info.append(info2)
            y.close()
            return info
    def ratingButton2(self):
        s=self.connection
        hotel=self.ratingBox.get(self.ratingBox.curselection())
        m=self.gettingInfo()
        username1=m[4]
        date1=m[2]
        time1=m[3]
        type1=m[0]
        capacity1=m[1]
        if tkMessageBox.askyesno("Send the venue a request","Do you want to send "+hotel+" a request?"):
             sendMessage(s,"rabutarb1","hotel:"+hotel+":usrname:"+username1+":date:"+date1+":time:"+time1+":type:"+type1+":capacity:"+capacity1)
             tkMessageBox.showinfo("Success","Your request has been sent. Please wait for the service provider to reply in the next 3 hours.")
    def locationButton2(self):
        s=self.connection
        hotel=self.locationBox.get(self.locationBox.curselection())
        m=self.gettingInfo()
        username1=m[4]
        date1=m[2]
        time1=m[3]
        type1=m[0]
        capacity1=m[1]
        if tkMessageBox.askyesno("Send the venue a request","Do you want to send "+hotel+" a request?"):
            sendMessage(s,"rabutarb1","hotel:"+hotel+":usrname:"+username1+":date:"+date1+":time:"+time1+":type:"+type1+":capacity:"+capacity1)
            tkMessageBox.showinfo("Sucess","Your request has been sent. Please wait for the service provider to reply in the next 3 hours.")
    def typeButton2(self):
        s=self.connection
        hotel=self.typeBox.get(self.typeBox.curselection())
        listInfo=self.gettingInfo()
        username1=m[4]
        date1=m[2]
        time1=m[3]
        type1=m[0]
        capacity1=m[1]
        if tkMessageBox.askyesno("Send the venue a request","Do you want to send "+hotel+" a request?"):
            sendMessage(s,"rabutarb1","hotel:"+hotel+":usrname:"+username1+":date:"+date1+":time:"+time1+":type:"+type1+":capacity:"+capacity1)
            tkMessageBox.showinfo("Sucess","Your request has been sent. Please wait for the service provider to reply in the next 3 hours.")
    def capacityButton2(self):
        s=self.connection
        hotel=self.capacityBox.get(self.capacityBox.curselection())
        m=self.gettingInfo()
        username1=m[4]
        date1=m[2]
        time1=m[3]
        type1=m[0]
        capacity1=m[1]
        if tkMessageBox.askyesno("Send the venue a request","Do you want to send "+hotel+" a request?"):
            sendMessage(s,"rabutarb1","hotel:"+hotel+":usrname:"+username1+":date:"+date1+":time:"+time1+":type:"+type1+":capacity:"+capacity1)
            tkMessageBox.showinfo("Success","Your request has been sent. Please wait for the service provider to reply in the next 3 hours.")
    def budgetButton2(self):
        s=self.connection
        hotel=self.budgetBox.get(self.budgetBox.curselection())
        m=self.gettingInfo()
        username1=m[4]
        date1=m[2]
        time1=m[3]
        type1=m[0]
        capacity1=m[1]
        if tkMessageBox.askyesno("Send the venue a request","Do you want to send "+hotel+" a request?"):
            sendMessage(s,"rabutarb1","hotel:"+hotel+":usrname:"+username1+":date:"+date1+":time:"+time1+":type:"+type1+":capacity:"+capacity1)
            tkMessageBox.showinfo("Success","our request has been sent. Please wait for the service provider to reply in the next 3 hours.")


        
        


#catering form
class catering:
    def __init__(self):
        self.connection=StartConnection("86.36.46.10", 15112)
        login (self.connection, "rabutarb2", "rabutarb")
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
        #cuisine selection
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
        #rating
        self.ratingLabel=Label(self.window5,text="Rating")
        self.ratingLabel.place(x=420,y=372)
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
        #Allergies
        self.allerLabel=Label(self.window5,text="Any allergies or type of food you don't want at your event?")
        self.allerLabel.place(x=520,y=572)
        self.allerEntry=Entry(self.window5)
        self.allerEntry.place(x=620,y=642)
        #submit button
        submitButton=Button(self.window5,text="Submit",command=self.submitButton2)
        submitButton.place(x=920,y=672)
        self.backButton=Button(self.window5,text="Go Back",command=self.backButton2)
        self.backButton.place(x=80,y=100)
        self.window5.mainloop()
    def backButton2(self):
        self.window5.destroy()
        m=eventMenu()
    def submitButton2(self):
        message=""
        cuisineM=""
        ratingM=""
        capacityM=""
        allergiesM=""
        s=self.connection
        cuisineM=self.variable.get()
        ratingM=self.variable2.get()
        allergiesM=self.allerEntry.get()
        f=open("temp.txt","r")
        info2=f.readlines()
        guests=info2[1]
        f.close()
        sendMessage(self.connection,"rabutarb1","catering:cuisine:"+cuisineM+":rating:"+ratingM+":capacity:"+guests+":allergies:"+allergiesM+"\n")
        allMessages = getMail(s)
        allMessages=allMessages[0]
        if allMessages!=[]:
            for i in allMessages:
                message=i[1]
                if "Cuisine" in message:
                    colonIndex=message.find(":")
                    cuisineM=message[colonIndex+1:]
                if "Rating" in message:
                    colonIndex=message.find(":")
                    ratingM=message[colonIndex+1:]
                if "Capacity" in message:
                    colonIndex=message.find(":")
                    capacityM=message[colonIndex+1:]
            m=cuisineWindow(cuisineM,ratingM,capacityM,allergiesM)
            return m

#catering results
class cuisineWindow:
    def __init__(self,cuisine,rating,capacity,allergies):
            self.connection=StartConnection("86.36.46.10", 15112)
            login (self.connection, "rabutarb2", "rabutarb")
            self.window5=Toplevel()
            self.bg = PhotoImage(file ="makechoice.gif")
            self.width=self.window5.winfo_screenwidth()
            self.height=self.window5.winfo_screenheight() 
            self.window5.geometry("%dx%d+0+0"%(self.width,self.height))
            self.window5.title("Cuisine")
            self.label1=Label(self.window5,image=self.bg)
            self.label1.grid()
            #boxes
            #values
            self.cuisine=cuisine.split("-")
            self.rating=rating.split("-")
            self.capacity=capacity.split("-")
            #cuisine
            cuisineLabel=Label(self.window5,text="Cuisine")
            cuisineLabel.place(x=260,y=180)
            cuisineButton=Button(self.window5,text="Select",command=self.cuisineButton2)
            cuisineButton.place(x=260,y=380)
            self.cuisineBox=Listbox(self.window5)
            self.cuisineBox.place(x=200,y=200)
            if self.cuisine==[ ]:
                self.ratingBox.insert(END,"No results for this cuisine")
            else:
                for r in range(len(self.cuisine)):
                    self.cuisineBox.insert(END,self.cuisine[r])
            #rating
            ratingLabel=Label(self.window5,text="Rating")
            ratingLabel.place(x=660,y=180)
            ratingButton=Button(self.window5,text="Select",command=self.ratingButton2)
            ratingButton.place(x=660,y=380)
            self.ratingBox=Listbox(self.window5)
            self.ratingBox.place(x=600,y=200)
            if self.rating==[]:
                self.ratingBox.insert(END,"No results for this rating")
            else:
                for r in range(len(self.rating)):
                    self.ratingBox.insert(END,self.rating[r])
   
            #capacity
            capacityLabel=Label(self.window5,text="Capacity")
            capacityLabel.place(x=460,y=380)
            capacityButton=Button(self.window5,text="Select",command=self.capacityButton2)
            capacityButton.place(x=460,y=580)
            self.capacityBox=Listbox(self.window5)
            self.capacityBox.place(x=400,y=400)
            if self.capacity==[]:
                self.capacityBox.insert(END,"No results for this capacity")
            else:
                for r in range(len(self.capacity)):
                    self.capacityBox.insert(END,self.capacity[r])
            self.window5.mainloop()
            
    def gettingInfo(self):
            info=[]
            f=open("temp.txt","r")
            info=f.readlines()
            f.close()
            y=open("username.txt","r")
            info2=y.readline()
            info.append(info2)
            y.close()
            return info
    def ratingButton2(self):
            s=self.connection
            cater=self.ratingBox.get(self.ratingBox.curselection())
            m=self.gettingInfo()
            username1=m[4]
            date1=m[2]
            time1=m[3]
            type1=m[0]
            capacity1=m[1]
            if tkMessageBox.askyesno("Send the catering service a request","Do you want to send "+hotel+" a request?"):
                 sendMessage(s,"rabutarb1","restu:"+cater+":usrname:"+username1+":date:"+date1+":time:"+time1+":type:"+type1+":capacity:"+capacity1)
                 tkMessageBox.showinfo("Success","Your request has been sent. Please wait for the service provider to reply in the next 3 hours.")
    def cuisineButton2(self):
            s=self.connection
            cater=self.cuisineBox.get(self.cuisineBox.curselection())
            m=self.gettingInfo()
            username1=m[4]
            date1=m[2]
            time1=m[3]
            type1=m[0]
            capacity1=m[1]
            if tkMessageBox.askyesno("Send the catering service a request","Do you want to send "+cater+" a request?"):
                 sendMessage(s,"rabutarb1","restu:"+cater+":usrname:"+username1+":date:"+date1+":time:"+time1+":type:"+type1+":capacity:"+capacity1)
                 tkMessageBox.showinfo("Success","Your request has been sent. Please wait for the service provider to reply in the next 3 hours.")

    def capacityButton2(self):
            s=self.connection
            cater=self.capacityBox.get(self.capacityBox.curselection())
            m=self.gettingInfo()
            username1=m[4]
            date1=m[2]
            time1=m[3]
            type1=m[0]
            capacity1=m[1]
            if tkMessageBox.askyesno("Send the catering service a request","Do you want to send "+cater+" a request?"):
                 sendMessage(s,"rabutarb1","restu:"+cater+":usrname:"+username1+":date:"+date1+":time:"+time1+":type:"+type1+":capacity:"+capacity1)
                 tkMessageBox.showinfo("Success","Your request has been sent. Please wait for the service provider to reply in the next 3 hours.")



firstWindow()
