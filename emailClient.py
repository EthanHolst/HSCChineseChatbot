import sqlite3 # library for connecting python code to the database of accounts/questions
import os # library for establishing paths for the chat log and database
from datetime import datetime # library for the current date, day and time for email subject
import smtplib # library to control interactions with the SMTP port to connect to Yahoo Mail
from email.message import EmailMessage # library to allow for email contents and attachments

# SMTP server connection client to send mail from
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587

# sets path as the folder this python file is in and then finds the accounts/questions database from that
path = os.path.dirname(os.path.abspath(__file__))
DBpath = os.path.join(path, 'QuestionDatabase.db')

# sets path as the folder this python file is in and then finds the chat log text file from that
txt_path = os.path.join(path, 'chatLog.txt')

def send_log_to_teacher(userID):
    # connects to SQL database through cursor
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor() 

    # finds the teacherID from the current user for email recipient
    code1 = ('SELECT TeacherID FROM Accounts WHERE AccountID = {id}').format(id = userID)
    cursor.execute(code1)
    teacherID = cursor.fetchall()
    teacherID = teacherID[0][0]
    
    # checks if the teacherID is above 0 to determie if the current user is a teacher
    # in this case there will be no email sent as the teacher is most likely just using the app for testing etc.
    # it would break the program if the function sent an email to a teacher which has no teacher
    if teacherID > 0:
        code = ('SELECT Email FROM Accounts WHERE AccountID = {id}').format(id = teacherID)
        cursor.execute(code)
        teacherEmail = cursor.fetchall()

        # finds the date and time for the Email subject
        now = datetime.now()
        current_time = now.strftime("%D - %H:%M")

        # finds the userID's username for the Email subject
        code = ('SELECT Username FROM Accounts where AccountID = {id}').format(id = userID)
        cursor.execute(code)
        username = cursor.fetchall()
        username = username[0][0]

        cursor.close()

        EMAIL_FROM = "hscchinesechatbot@yahoo.com"

        # emails to userID's teacher
        EMAIL_TO = teacherEmail[0][0]
        SMTP_USERNAME = "hscchinesechatbot"
        SMTP_PASSWORD = "fqrwncqrmuqghmtn"

        # formats subject to give details on when log finished as well as the user whose log it is
        EMAIL_SUBJECT = "{user}\'s log from session ({date})".format(user = username, date = current_time)         
        
        # composes the parts of email in the EmailMessage library
        # adds attachment of chatLog
        # connects to the server and logs in with the hardcoded email account details
        # sends email to the teacher from the application address with the subject and file attached

        msg = EmailMessage()
        msg['Subject'] = EMAIL_SUBJECT + ""
        msg['From'] = EMAIL_FROM 
        msg['To'] = EMAIL_TO
        msg.add_attachment(open(txt_path, "r", encoding='utf-8').read(), filename="chatLog.txt")
        debuglevel = True
        mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        mail.set_debuglevel(debuglevel)
        mail.starttls()
        mail.login(SMTP_USERNAME, SMTP_PASSWORD)
        mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        mail.quit()
