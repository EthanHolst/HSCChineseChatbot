import sqlite3 #library for connecting python code to the database of accounts/questions
import os # library for establishing paths for the chat log and database

# sets path as the folder this python file is in and then finds the accounts/questions database from that
path = os.path.dirname(os.path.abspath(__file__))
DBpath = os.path.join(path, 'QuestionDatabase.db')

# function that takes an input and category and inserts it into the followup question table
def addFollowup(input, category):
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor() 
    cursor.execute("INSERT INTO FollowupQuestions (QuestionText, Category) VALUES (?, ?)", (input, category))
    connect.commit()
    cursor.close()

# function that takes the username and password and checks if it exists with password case sensitivity
# returns if the account exists through a boolean
def login(username, password):
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor() 

    cursor.execute('SELECT Username, Password from Accounts')
    accounts = cursor.fetchall()

    accountFound = False
    i = 0
    while accountFound == False and i < len(accounts):
        if (accounts[i][0].lower() == username.lower() and accounts[i][1] == password):
            accountFound = True
            break
        i = i + 1
    
    cursor.close()
    return accountFound
    
# function that takes a passed email, username and password
# then takes all emails and usernames that exist in the Account database before checking if they already have accounts without case sensitivity
# if it doesn't exist it inputs it into the database and returns if the account exists as a boolean
def signup(email, username, password):
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor() 
    cursor.execute('SELECT Email, Username, Password from Accounts')
    accounts = cursor.fetchall()
    cursor.close()

    accountFound = False
    i = 0
    while accountFound == False and i < len(accounts):
        if (accounts[i][0].lower() == email.lower() or accounts[i][1].lower() == username.lower()):
            accountFound = True
            break
        i = i + 1   
    
    if (accountFound == False):
        conn = sqlite3.connect(DBpath)
        cursor = conn.cursor() 
        cursor.execute("INSERT INTO Accounts (Email, Username, Password) VALUES (?, ?, ?)", (email, username, password))
        conn.commit()
        cursor.close()

    return accountFound

# function that takes the userID, account type, schoolId, and teacherID before checking if the account is a teacher
# if the account is a teacher is inputs their teacherID as 0, and if not it inputs the selected teacherID
def signup_secondary(userID, account_type, schoolID, teacherID):
        conn = sqlite3.connect(DBpath)
        cursor = conn.cursor() 
        if teacherID != 0:
            cursor.execute(("UPDATE Accounts SET AccountType = '{AccountType}', School = {schID} , TeacherID = {tchID} WHERE AccountID = {id}").format(id = userID, AccountType = account_type, schID = schoolID, tchID = teacherID))
        else:
            cursor.execute(("UPDATE Accounts SET AccountType = '{AccountType}', School = {schID}, TeacherID = 0 WHERE AccountID = {id}").format(id = userID, AccountType = account_type, schID = schoolID))
        conn.commit()
        cursor.close()

# function that retrieves the schoolnames from the School table in the database
# it then cleans the database output so it can be cleanly inputted into the option box within the Tkinter GUI
# returns the clean school array
def retrieve_schools():
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor()

    cursor.execute('SELECT SchoolName FROM Schools')
    schools = cursor.fetchall()
    cursor.close()

    schools_clean = ["Select school"]
    for i in schools:
        schools_clean.append(i[0])
        
    return schools_clean

# function that is passed the school name and userID
# it finds all teachers that teach at the inputted school name
# it then adds all teachers of that school into an array unless they have the same userID as the user, meaning a user cannot teach themselves
# it then cleans the database output so it can be cleanly inputted into the option box within the Tkinter GUI
# returns the clean teacher array
def retrieve_teachers(schoolName, userID):
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor()
    cursor.execute(('SELECT SchoolID FROM Schools WHERE SchoolName = "{name}"').format(name=schoolName))
    schoolID = cursor.fetchall()

    cursor.execute(('SELECT Username FROM Accounts WHERE School = {schID} AND AccountType = "Teacher" AND AccountID != {userID}').format(schID = schoolID[0][0], userID = userID))
    teachers = cursor.fetchall()
    cursor.close()

    teachers_clean = ["Select teacher"]
    for i in teachers:
        teachers_clean.append(i[0])
        
    return teachers_clean

# function that retrieves the userID from the username and then returns it
def retrieve_userID(userName):
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor()
    cursor.execute(('SELECT AccountID FROM Accounts WHERE Username = "{name}"').format(name=userName))
    userID = cursor.fetchall()
    cursor.close()

    return userID[0][0]

# function that retrieves the schoolID from the school name and then returns it
def retrieve_schoolID(schoolName):
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor()
    cursor.execute(('SELECT SchoolID FROM Schools WHERE SchoolName = "{name}"').format(name=schoolName))
    schoolID = cursor.fetchall()
    cursor.close()

    return schoolID[0][0]

# function that verifies if a user is a teacher or not, allowing for certain permisisons and access to functions in the Tkinter GUI
def teacherVerify(userID):
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor()
    code1 = ('SELECT TeacherID FROM Accounts WHERE AccountID = {id}').format(id = userID)
    cursor.execute(code1)
    teacherID = cursor.fetchall()
    teacherID = teacherID[0][0]
    cursor.close()

    if teacherID > 0:
        return False
    else:
        return True