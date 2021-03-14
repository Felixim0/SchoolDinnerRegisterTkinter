from tkinter import *
import sqlite3
import smtplib
import datetime
root=Tk()                                                                        # Makes Tk window root

sizex = 1000
sizey = 800    
root.wm_geometry("%dx%d" % (sizex, sizey))                                       # Sets the size of window
root.resizable(False, False)

font = ("Times", 16)

connection = sqlite3.connect('./database1.db')
cursor = connection.cursor()
frame= Frame(root)   
def loginScreen(pframe):
    pframe.destroy()
    loginScreenFrame = Frame(root,width=sizex, height=sizey)
    loginScreenFrame.pack()

    centeredFrame = Frame(loginScreenFrame,highlightbackground="Blue", highlightthickness=7)
    centeredFrame.place(relx=.5, rely=.5, anchor="center")

    loginStuffFrame = Frame(centeredFrame)
    loginStuffFrame.grid(row=0,column=0)

    loginLabel = Label(loginStuffFrame,text="Login",font=str(font[0] + ", 40"))
    loginLabel.grid(row=0,column=0,columnspan = 2,pady = 50)

    userNameEntry = Entry(loginStuffFrame,font=font,borderwidth=4)
    userNameEntry.grid(row=1,column=1)

    userNameLabel = Label(loginStuffFrame,font=font,text="Username ")
    userNameLabel.grid(row=1,column=0)

    passwordEntry = Entry(loginStuffFrame,font=font,borderwidth=4,show="*")
    passwordEntry.grid(row=2,column=1,pady = 15,padx = 10)

    passwordLabel = Label(loginStuffFrame,font=font,text="Password ")
    passwordLabel.grid(row=2,column=0,pady = 15,padx = 10)

    enterButton = Button(loginStuffFrame,font=str(font[0] + ", 30"),text = "Login", command = lambda: checkLogin(userNameEntry.get(),passwordEntry.get(),loginScreenFrame))
    enterButton.grid(row = 4, column = 0 ,columnspan = 2, pady = 30)

    root.mainloop()
    
def checkLogin(userName,password,pFrame):
    query = ("SELECT * FROM teacherData WHERE userName = '" + str(userName) + "' AND password = '" + str(password) + "'")
    cursor.execute(query)
    user = []
    for row in cursor:
        user.append(row[:])
    if len(user) > 1:
        print("2 identical users smh")
    elif len(user) == 0:
        print("user/passwd not found")

    else:
        mainMenu(user[0],pFrame)

def mainMenu(userData,pFrame="Null"):
    if pFrame != "Null":
        pFrame.destroy()
    mmFrame = Frame(root,width=sizex, height=sizey)
    mmFrame.pack()
    centeredFrame = Frame(mmFrame,highlightbackground="Blue", highlightthickness=7)
    centeredFrame.place(relx=.5, rely=.5, anchor="center")
    titleLabel = Label(centeredFrame,text="Main Menu",font=str(font[0] + ", 40"))
    titleLabel.grid(row=0,column=1,columnspan = 2,pady = 50)

    buttonHeight = 3
    buttonWidth = 10
    Button(centeredFrame,font=font,text="Logout",command=lambda:loginScreen(mmFrame),height=buttonHeight,width = buttonWidth).grid(row=3,column=2,padx=10,pady=10)      

    availableStudentsFrame=Frame(centeredFrame,relief=GROOVE,width=2000,height=4000,bd=3)                 
    availableStudentsFrame.grid(column=1,row=1,rowspan=4,padx=10,pady=10)
    movingCanvas=Canvas(availableStudentsFrame)                                                                              
    frame=Frame(movingCanvas)                     
                                                 
    scrollbar=Scrollbar(availableStudentsFrame,orient="vertical")      
    movingCanvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.config(command=movingCanvas.yview)                    
    scrollbar.pack(side="right",fill="y")                          
    movingCanvas.pack(side="left")                                             
    movingCanvas.create_window((0,0),window=frame,anchor='nw')
    x=0
    frame.bind("<Configure>",lambda x: moveCanvas(movingCanvas))
    moveCanvas(movingCanvas)
    
    frameForButtons = Frame(frame)                                                                                           
    frameForButtons.pack()

    query = ("SELECT * FROM classData WHERE teacherID = '" + str(userData[0]) + "'")
    cursor.execute(query)
    childIDs = []
    for row in cursor:
        childIDs.append(row[0])
        
    classData = []
    if len(childIDs) > 0:
        
        query = ("SELECT * FROM studentData WHERE ")
        for studentID in childIDs:
            query = str(query) + " studentID = '" + str(studentID) + "' OR " 
        query = query[:-3]
        
        query = query + " ORDER BY firstName ASC"
#       print(query)
        cursor.execute(query)
        for row in cursor:
            classData.append(row[:])

            #convert into an array
        classArray = []
        for studentData in classData:
            tempArray = []
            for eachBitOfData in studentData:
                tempArray.append(eachBitOfData)
            classArray.append(tempArray[:])
    
    classData = classArray[:]
    makeButtons(classData,frame,frameForButtons)

    Button(centeredFrame,font=font,text="Add Student",command=lambda:createNewPerson(mmFrame,userData),height=buttonHeight,width = buttonWidth).grid(row=1,column=2,padx=10,pady=10)
    Button(centeredFrame,font=font,text="Save List",command=lambda:saveList(mmFrame,userData),height=buttonHeight,width = buttonWidth).grid(row=2,column=2,padx=10,pady=10)

def saveList(pFrame,userData):
    global saveableClassData
# dinnerMenuForMo@gmail.com
# moham2DinnerMenu!

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("dinnerMenuForMo", "moham2DinnerMenu!")
    
    currentDate = str(datetime.date.today())

    msg = str(currentDate) + "\n"
    tmp = ""
    for eachStudent in saveableClassData:
        tmp = tmp + str(eachStudent[1]) + " " + str(eachStudent[2]) + spaceCreator(eachStudent) + str(eachStudent[3]) + "\n"

    msg = msg + tmp
    print(msg)

    server.sendmail("dinnerMenuForMo@gmail.com", "12mnaji@jogschool.org", msg)
        
    server.quit()

    
    print(saveableClassData)
    
def spaceCreator(eachStudent):
    string = (str(eachStudent[1]) + " " + str(eachStudent[2]))
    comparison=24

    exactNumberOfSpaces=(":")
    spaceNumber=comparison-(int(len(string)))
    x = exactNumberOfSpaces.ljust(spaceNumber)

    return(x)
    
saveableClassData = []
def makeButtons(classData,frame,frameForButtons):
    global saveableClassData
    saveableClassData = classData[:]
    if classData != []:
        for i in range(0,len(classData)):
            if len(classData) != 0:
                Label(frameForButtons,text=str(str(classData[i][1]) + " " + str(classData[i][2])),font=font,width=20,anchor=W).grid(row=i,column=1,padx=4,pady=3)
                if (classData[i][3] == "V"):            
                    Button(frameForButtons,text="V",font=font,anchor=W,command = lambda i=i: setStudentPrefference(classData,i,"V",frame,frameForButtons),bg = "light green").grid(row=i,column=2,padx=2,pady=2)
                else:
                    Button(frameForButtons,text="V",font=font,anchor=W,command = lambda i=i: setStudentPrefference(classData,i,"V",frame,frameForButtons)).grid(row=i,column=2,padx=2,pady=2)
                
                if (classData[i][3] == "M"):            
                    Button(frameForButtons,text="M",font=font,anchor=W,command = lambda i=i: setStudentPrefference(classData,i,"M",frame,frameForButtons),bg = "light green").grid(row=i,column=3,padx=2,pady=2)
                else:
                    Button(frameForButtons,text="M",font=font,anchor=W,command = lambda i=i: setStudentPrefference(classData,i,"M",frame,frameForButtons)).grid(row=i,column=3,padx=2,pady=2)               
                
                if (classData[i][3] == "O"):            
                    Button(frameForButtons,text="O",font=font,anchor=W,command = lambda i=i: setStudentPrefference(classData,i,"O",frame,frameForButtons),bg = "light green").grid(row=i,column=4,padx=2,pady=2)
                else:
                    Button(frameForButtons,text="O",font=font,anchor=W,command = lambda i=i: setStudentPrefference(classData,i,"O",frame,frameForButtons)).grid(row=i,column=4,padx=2,pady=2)            

                if (classData[i][4] == "paid"):
                    Button(frameForButtons,text="P",font=font,anchor=W,command = lambda i=i:
                           setStudentPaid(classData,i,"notPaid",frame,frameForButtons),bg = "light green").grid(row=i,column=5,padx=14,pady=2)
                else:
                    Button(frameForButtons,text="P",font=font,anchor=W,command = lambda i=i:
                           setStudentPaid(classData,i,"paid",frame,frameForButtons)).grid(row=i,column=5,padx=14,pady=2)                    
    else:
        Label(frameForButtons,text="No Results Found",font=(font[0],int(font[1]*1.5))).grid(row=0,column=0)

def setStudentPaid(classData,index,toSet,frame,frameForButtons):
    classData[index][4] = str(toSet)
    frameForButtons.destroy()
    frameForButtons = Frame(frame)
    frameForButtons.pack()
    makeButtons(classData,frame,frameForButtons)

def setStudentPrefference(classData,index,option,frame,frameForButtons):
    classData[index][3] = str(option)
    frameForButtons.destroy()
    
    frameForButtons = Frame(frame)                                                                                           
    frameForButtons.pack()
    makeButtons(classData,frame,frameForButtons)


def createNewPerson(pFrame,userData):
    pFrame.destroy()
    centeredFrame = Frame(root,highlightbackground="Blue", highlightthickness=5)
    centeredFrame.place(relx=.5,rely=.5, anchor="center")    
    createNewPersonFrame = Frame(centeredFrame)
    createNewPersonFrame.grid(row=0,column=0,padx=10,pady=10)

    Label(createNewPersonFrame,text="First Name: ", font = ("Helvetica", 20)).grid(row=1,column=1)
    firstNameEntryBox = Entry(createNewPersonFrame, font = ("Helvetica", 20))
    firstNameEntryBox.grid(row = 1,column = 2)
    
    Label(createNewPersonFrame,text="Second Name: ", font = ("Helvetica", 20)).grid(row=2,column=1)
    lastNameEntryBox = Entry(createNewPersonFrame, font = ("Helvetica", 20))
    lastNameEntryBox.grid(row = 2,column = 2)
    
    Button(createNewPersonFrame, text="Enter", font = ("Helvetica", 20),command = lambda:
           addPersonToDatabase(str(firstNameEntryBox.get()),str(lastNameEntryBox.get()),userData)).grid(row=1,column=3,padx=10,pady=10)
    
    Button(createNewPersonFrame, text="Back", font = ("Helvetica", 20),command = lambda: mainMenu(userData)).grid(row=2,column=3,padx=10,pady=10)

def addPersonToDatabase(firstName,lastName,userData):
    if (firstName != "") and (lastName != ""):
        query = ("INSERT INTO studentData (firstName,secondName) VALUES ('" + str(firstName) + "','" + str(lastName) + "')")
        cursor.execute(query)
        connection.commit()
        mainMenu(userData)

def moveCanvas(canvasForButtons):
    canvasForButtons.configure(scrollregion=canvasForButtons.bbox("all"),width=400,height=300)

if __name__ == "__main__":
    loginScreen(frame)
    root.mainloop()

