
#    15-112: Principles of Programming and Computer Science
#    HW07 Programming: Implementing a Chat Client
#    Name      : Rahaf Khaled
#    AndrewID  : rabutarb

#    File Created: 28/10/2018
#    Modification History:
#    Start 28/10/2018-6:11 pm            End 28/10/2018-8:40pm
#    Start 1/11/2018-4:00pm              End 1/11/2018-8:00pm
#    Start 5/11/2018-1:30pm              End 5/11/2018-3:00pm
#    Start 7/11/2018-4:00pm              End 7/11/2018-6:46pm

import socket
import Tkinter
import pickle

########## USE THIS SPACE TO WRITE YOUR HELPER FUNCTIONS ##########
#Checks if length of message is 2 integers then adds a preceding 0
#If its length is 3 then it doesn't add a 0
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

########## FILL IN THE FUNCTIONS TO IMPLEMENT THE CLIENT ##########
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
 

def sendMessage(s, friend, message):
    #finds the size and converts it to a string
    size=str(6+len("@sendmsg")+1+len(friend)+1+len(message))
    size2=lengthOfSize(size)
    s.send("@"+size2+"@sendmsg@"+friend+"@"+message)
    answer=s.recv(512)
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
    answer=s.recv(512).strip()
    if int(answer[1:6]) > 512:
            readNext = int(answer[1:6])/512
            for i in range(readNext):
                answer += s.recv(512*readNext).strip()
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
        
   
   

def SendMessage(s):
    friend = raw_input("Please insert the username of the friend you would like to message: ")
    message = raw_input("Please insert the message that you would like to send: ")
    if friend in getFriends(s):
        if sendMessage(s, friend, message): print "Mesage sent to " + friend + " succesfully"
        else: "Error sending message to " + friend + ". Please try again."
    else: print friend, "is not a Friend. You must add them as a friend before you can message them."


username="rabutarb1"
password="rabutarb"

s=StartConnection("86.36.46.10", 15112)
login(s,"rabutarb1","rabutarb")
    
allMessages=[]
# Now user is logged in
def validateLogin(s,message1):
        message=message1
        username1=message[17:]
        atAfterUser=username1.find(":")
        actualUsername=username1[:atAfterUser]
        actualPassword=username1[atAfterUser+9:]
        fullUserAndPass="("+actualUsername+","+actualPassword+")"
        if message[:12]=="loginplanner":
            f=open("planneraccounts.txt","r")
            for line in f:
                if line.strip()==fullUserAndPass:
                   return sendMessage(s,"rabutarb2","Yes")
            f.close()
            return sendMessage(s,"rabutarb2","No")
            
                
        elif message[:12]=="loginservice":
            f=open("serviceaccounts.txt","r")
            for line in f:
                if line.strip()==fullUserAndPass:
                    return sendMessage(s,"rabutarb2","Yes")
            f.close()
            return sendMessage(s,"rabutarb2","No")

#helper function that checks if the username already exists
def ifExists(username):
    f=open("planneraccounts.txt","r")
    line=f.readline()
    while line:
        if line==username:
            return True
        else:
            return False

 
def signUp(s,message1):
        message=message1
        username1=message[18:]
        atAfterUser=username1.find(":")
        actualUsername=username1[:atAfterUser]
        actualPassword=username1[atAfterUser+9:]
        fullUserAndPass="("+actualUsername+","+actualPassword+")"
        if message[:13]=="signupplanner":
            if ifExists(actualUsername)==True:
                return sendMessage(s,"rabutarb2","no")
            else:
                f=open("planneraccounts.txt","a")
                f.write(fullUserAndPass+"\n")
                f.close()
                return sendMessage(s,"rabutarb2","ok")


#get message from user with specifications of venue,send back results that match
def venue(s,message1):
        message=message1
       #message decoded
        venue1=message[11:]
        findColonBeforeRating=venue1.find(":")
        actualType=venue1[:findColonBeforeRating]
        rating1=venue1[len(actualType)+8:]
        findColonBeforeLocation=rating1.find(":")
        actualRating=rating1[:findColonBeforeLocation]
        location1=rating1[len(actualRating)+10:]
        findColonBeforeBudget=location1.find(":")
        actualLocation=location1[:findColonBeforeBudget]
        budget1=location1[len(actualLocation)+8:]
        findColonBeforeCapacity=budget1.find(":")
        actualBudget=budget1[:findColonBeforeCapacity]
        actualCapacity=budget1[len(actualBudget)+10:]
        with open("hotels.txt") as f:
            content = f.read().splitlines()
        List=[l.split(',') for l in ','.join(content).split('/////')]
        for i in List:
            for j in i:
                if len(j)<1:
                    i.remove(j)
        for i in List:
            if i==[]:
                List.remove(i)
        List.pop(-1)
        
        hotelList=[]
        names=""
        for i in List:
            for j in i:
                if actualType in j:
                    if i[0] not in hotelList:
                        hotelList.append(i[0])
                        names="-".join(hotelList)
        sendMessage(s,"rabutarb2","Types:"+names)
        
        hotelList=[]
        names=""
        for i in List:
            for j in i:
                if actualRating in j:
                    if i[0] not in hotelList:
                        hotelList.append(i[0])
                        names="-".join(hotelList)
        sendMessage(s,"rabutarb2","Rating:"+names)
        
      
        hotelList=[]
        names=""
        for i in List:
            for j in i:
                if actualLocation in j:
                    if i[0] not in hotelList:
                        hotelList.append(i[0])
                        names="-".join(hotelList)
        sendMessage(s,"rabutarb2","Location:"+names)
        
        hotelList=[]
        names=""
        for i in List:
            for j in i:
                if j.isdigit():
                    cap=int(j)
                    if (int(actualCapacity)-100)<=cap<=(int(actualCapacity)+100):
                        if i[0] not in hotelList:
                            hotelList.append(i[0])
                            names="-".join(hotelList)
        sendMessage(s,"rabutarb2","Capacity:"+names)
       
        hotelList=[]
        names=""
        for i in List:
            for j in i:
                if j.isdigit():
                    eIndex=i.index(j)
                    bud=int(i[eIndex+1][:-1])
                    if (int(actualBudget)-100)<=bud<=(int(actualBudget)+100):
                        if i[0] not in hotelList:
                            hotelList.append(i[0])
                            names="-".join(hotelList)

        return sendMessage(s,"rabutarb2","Budget:"+names)

#Sending a message with all info about event to hotels                                       
def hotels(s,message1):
    message=message1
    #message decoded
    hotel2=message[6:]
    findColonBeforeUsername=hotel2.find(":")
    actualHotel=hotel2[:findColonBeforeUsername]
    username2=message[15+len(actualHotel):]
    findColonBeforeDate=username2.find(":")
    actualUsername=username2[:findColonBeforeDate]
    date2=username2[findColonBeforeDate+6:]
    findColonBeforeTime=date2.find(":")
    actualDate=date2[:findColonBeforeTime]
    time2=date2[findColonBeforeTime+6:]
    findColonBeforeType=time2.find(":")
    actualTime=time2[:findColonBeforeType]
    type2=time2[findColonBeforeType+6:]
    findColonBeforeCapacity=type2.find(":")
    actualType=type2[:findColonBeforeCapacity]
    actualCapacity=type2[findColonBeforeCapacity+10:]
    #send message to service provider
    mList=[actualHotel,actualUsername,actualType,actualDate,actualTime,actualCapacity]
    mString="-".join(mList)
    return sendMessage(s,"rabutarb3",mString)


def catering(s,message1):
    message=message1
    #message decoded
    cuisine1=message[17:]
    findColonBeforeRating=cuisine1.find(":")
    actualCuisine=cuisine1[:findColonBeforeRating]
    rating1=cuisine1[len(actualCuisine)+8:]
    findColonBeforeBudget=rating1.find(":")
    actualRating=rating1[:findColonBeforeBudget]
    capacity1=rating1[len(actualRating)+10:]
    findColonBeforeAller=capacity1.find(":")
    actualCapacity=capacity1[:findColonBeforeAller]
    actualAller=capacity1[len(actualCapacity)+11:]

    with open("food.txt") as f:
        content = f.read().splitlines()
    List=[l.split(',') for l in ','.join(content).split('/////')]
    for i in List:
        for j in i:
            if len(j)<1:
                i.remove(j)
    for i in List:
        if i==[]:
            List.remove(i)
    List.pop(-1)
    
    foodList=[]
    names=""
    for i in List:
        for j in i:
            if actualCuisine in j:
                if i[0] not in foodList:
                    foodList.append(i[0])
                        names="-".join(foodList)
    
    sendMessage(s,"rabutarb2","Cuisine:"+names)
       
    foodList=[]
    names=""
    for i in List:
        for j in i:
            if actualRating in j:
                if i[0] not in foodList:
                    foodList.append(i[0])
                        names="-".join(foodList)
    
    sendMessage(s,"rabutarb2","Rating:"+names)
            
    foodList=[]
    names=""
    for i in List:
        for j in i:
            if j.isdigit():
                cap=int(j)
                    if int(actualCapacity)<cap:
                        if i[0] not in foodList:
                            foodList.append(i[0])
                                names="-".join(foodList)
    
    return sendMessage(s,"rabutarb2","Capacity:"+names)


def resturants(s,message1):
    message=message1
    #message decoded
    hotel2=message[6:]
    findColonBeforeUsername=hotel2.find(":")
    actualHotel=hotel2[:findColonBeforeUsername]
    username2=message[15+len(actualHotel):]
    findColonBeforeDate=username2.find(":")
    actualUsername=username2[:findColonBeforeDate]
    date2=username2[findColonBeforeDate+6:]
    findColonBeforeTime=date2.find(":")
    actualDate=date2[:findColonBeforeTime]
    time2=date2[findColonBeforeTime+6:]
    findColonBeforeType=time2.find(":")
    actualTime=time2[:findColonBeforeType]
    type2=time2[findColonBeforeType+6:]
    findColonBeforeCapacity=type2.find(":")
    actualType=type2[:findColonBeforeCapacity]
    actualCapacity=type2[findColonBeforeCapacity+10:]
    #send message to service provider
    mList=[actualHotel,actualUsername,actualType,actualDate,actualTime,actualCapacity]
    mString="-".join(mList)
    return sendMessage(s,"rabutarb3",mString)
    

def mainFunction(sock):
    message=""
    allMessages = getMail(s)
    allMessages = allMessages[0]
    if allMessages!=[]:
        for i in allMessages:
            message=i[1]
    if "login" in message:
        validateLogin(sock,message)
    if "signup" in message:
        signUp(sock,message)
    if "venue" in message:
        venue(sock,message)
    if "hotel" in message:
        hotels(sock,message)
    if "catering" in message:
        catering(sock,message)
    if "restu" in message:
        resturants(sock,message)

while True:
    mainFunction(s)
    
    




