import sqlite3
import os

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
    cursor.close()

    accountFound = False
    i = 0
    while accountFound == False and i < len(accounts):
        if (accounts[i][0].lower() == username.lower() and accounts[i][1] == password):
            print("stub: log in successsful")
            accountFound = True
            break
        i = i + 1
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
            print("stub: account username or password already exists")
            accountFound = True
            break
        i = i + 1   
    
    if (accountFound == False):
        connect = sqlite3.connect(DBpath)
        cursor = connect.cursor() 
        cursor.execute("INSERT INTO Accounts (Email, Username, Password, AccountType) values (?, ?, ?)", (email, username, password))
        cursor.close()
