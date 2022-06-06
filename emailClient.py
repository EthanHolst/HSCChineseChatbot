from numpy import character
import win32com.client as win32
import sqlite3
import os
from datetime import datetime

#stub
userID = 2

path = os.path.dirname(os.path.abspath(__file__))
DBpath = os.path.join(path, 'QuestionDatabase.db')
txt_path = os.path.join(path, 'chatLog.txt')

def send_log_to_teacher():
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor() 

    """ Retrieve Teacher Email based off AccountID"""
    code1 = ('SELECT TeacherID FROM Accounts WHERE AccountID = {id}').format(id = userID)
    cursor.execute(code1)
    teacherID = cursor.fetchall()
    teacherID = teacherID[0][0]
    code = ('SELECT Email FROM Accounts WHERE AccountID = {id}').format(id = teacherID)
    cursor.execute(code)
    teacherEmail = cursor.fetchall()

    now = datetime.now()
    current_time = now.strftime("%D - %H:%M")
    code = ('SELECT Username FROM Accounts where AccountID = {id}').format(id = userID)
    cursor.execute(code)
    username = cursor.fetchall()
    username = username[0][0]

    cursor.close()

    to = teacherEmail[0][0]

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = "{user}\'s log from session ({date})".format(user = username, date = current_time)
    mail.To = to 
    mail.Attachments.Add(txt_path)
    mail.HTMLBody = r"""
    Please find the attatched log below
    """
    mail.Send()


send_log_to_teacher()