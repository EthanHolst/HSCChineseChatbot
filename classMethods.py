import sqlite3
import os
import Main

path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, 'QuestionDatabase.db')

def addFollowup(Text, Cat):
    conn = sqlite3.connect(db)
    cursor = conn.cursor() 
    cursor.execute('SELECT COUNT(*) from FollowupQuestions')
    cursorResult = cursor.fetchone()
    QuesID = cursorResult[0] + 1

    cursor.execute("insert into FollowupQuestions (QuestionID, QuestionText, Category) values (?, ?, ?)", (QuesID, Text, Cat))
    conn.commit()
    cursor.close()

def removeFollowup(QuestionID):
    conn = sqlite3.connect(db)
    cursor = conn.cursor() 

    code = ('DELETE FROM FollowupQuestions WHERE QuestionID = {id}').format(id = QuestionID)
    cursor.execute(code)

    cursor.close()

removeFollowup(10)