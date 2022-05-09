from cgitb import text
import sqlite3
import os

path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, 'QuestionDatabase.db')
conn = sqlite3.connect(db)
cursor = conn.cursor() 

def addFollowup(Text, Cat):
    cursor.execute('SELECT COUNT(*) from FollowupQuestions')
    cursorResult = cursor.fetchone()
    QuesID = cursorResult[0] + 1

    cursor.execute("insert into FollowupQuestions (QuestionID, QuestionText, Category) values (?, ?, ?)", (QuesID, Text, Cat))
    conn.commit()
    cursor.close()

addFollowup("我很喜欢我的中文老师。",1)