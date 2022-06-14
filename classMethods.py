import sqlite3
import os

import globals
import Main

globals.initialise()
userID = globals.num

path = os.path.dirname(os.path.abspath(__file__))
DBpath = os.path.join(path, 'QuestionDatabase.db')

def addFollowup(Text, Cat):
    conn = sqlite3.connect(DBpath)
    cursor = conn.cursor() 
    cursor.execute('SELECT COUNT(*) from FollowupQuestions')
    cursorResult = cursor.fetchone()
    QuesID = cursorResult[0] + 1

    cursor.execute("INSERT INTO FollowupQuestions (QuestionID, QuestionText, Category) VALUES (?, ?, ?)", (QuesID, Text, Cat))
    conn.commit()
    cursor.close()

# unfinished (not working)
def removeFollowup(QuestionID):
    conn = sqlite3.connect(DBpath)
    cursor = conn.cursor() 

    code = ('DELETE FROM FollowupQuestions WHERE QuestionID = {id}').format(id = QuestionID)
    cursor.execute(code)

    cursor.close()

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
    
    cursor.execute(('SELECT AccountID FROM Accounts WHERE Username = "{id}"').format(id = accounts[i][0]))
    login_ID = cursor.fetchall()
    cursor.close()

    globals.num = login_ID
    return accountFound
    
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
            print("Acc exists")
            accountFound = True
            break
        i = i + 1   
    
    if (accountFound == False):
        conn = sqlite3.connect(DBpath)
        cursor = conn.cursor() 
        cursor.execute('SELECT COUNT(*) from Accounts')
        cursorResult = cursor.fetchone()
        accountID = cursorResult[0] + 1

        cursor.execute("INSERT INTO Accounts (AccountID, Email, Username, Password) VALUES (?, ?, ?, ?)", (accountID, email, username, password))
        conn.commit()
        cursor.close()

    return accountFound

def signup_secondary(account_type, schoolID, teacher):
        conn = sqlite3.connect(DBpath)
        cursor = conn.cursor() 
        if teacher != 0:
            cursor.execute(("UPDATE Accounts SET AccountType = '{AccountType}', School = {schID} , TeacherID = {tchID} WHERE AccountID = {id}").format(id = globals.num, AccountType = account_type, schID = schoolID, tchID = teacher))
        else:
            cursor.execute(("UPDATE Accounts SET AccountType = '{AccountType}', School = {schID} WHERE AccountID = {id}").format(id = globals.num, AccountType = account_type, schID = schoolID))
        conn.commit()
        cursor.close()

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

def retrieve_teachers(schoolName):
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor()
    cursor.execute(('SELECT SchoolID FROM Schools WHERE SchoolName = "{name}"').format(name=schoolName))
    schoolID = cursor.fetchall()

    cursor.execute(('SELECT Username FROM Accounts WHERE School = {id} AND AccountType = "Teacher"').format(id = schoolID[0][0]))
    teachers = cursor.fetchall()
    cursor.close()

    teachers_clean = ["Select teacher"]
    for i in teachers:
        teachers_clean.append(i[0])
        
    return teachers_clean

def retrieve_userID(userName):
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor()
    cursor.execute(('SELECT AccountID FROM Accounts WHERE Username = "{name}"').format(name=userName))
    userID = cursor.fetchall()
    cursor.close()

    return userID[0][0]

def retrieve_schoolID(schoolName):
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor()
    cursor.execute(('SELECT SchoolID FROM Schools WHERE SchoolName = "{name}"').format(name=schoolName))
    schoolID = cursor.fetchall()
    cursor.close()

    return schoolID[0][0]