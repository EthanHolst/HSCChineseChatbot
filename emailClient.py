import sqlite3
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587

path = os.path.dirname(os.path.abspath(__file__))
DBpath = os.path.join(path, 'QuestionDatabase.db')
txt_path = os.path.join(path, 'chatLog.txt')

def send_log_to_teacher(userID):
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

    co_msg = "Please find the attatched log below"
    EMAIL_FROM = "hscchinesechatbot@yahoo.com"
    EMAIL_TO = teacherEmail[0][0]
    SMTP_USERNAME = "hscchinesechatbot@yahoo.com"
    SMTP_PASSWORD = "fqrwncqrmuqghmtn"
    EMAIL_SUBJECT = "{user}\'s log from session ({date})".format(user = username, date = current_time)
    msg = MIMEText(co_msg)
    msg['Subject'] = EMAIL_SUBJECT + ""
    msg['From'] = EMAIL_FROM 
    msg['To'] = EMAIL_TO
    msg.attach(txt_path)
    debuglevel = True
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()


    send_log_to_teacher(3)