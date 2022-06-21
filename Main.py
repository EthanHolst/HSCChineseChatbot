from cgitb import text
import jieba
import math
import sqlite3
import os
import random
from datetime import datetime
import io

path = os.path.dirname(os.path.abspath(__file__))
DBpath = os.path.join(path, 'QuestionDatabase.db')
txt_path = os.path.join(path, 'chatLog.txt')

def userInput():
    clear_existing_log()
    """ Retrieves categories from DB. """
    print("")
    print(retrieveCategories())
    Category = input("Please input the CategoryID of what the category question you would like: ") 
    print(retrieveOriginalQes(Category))
    followupApproximation(Category)

def clear_existing_log():
    log_path = os.path.join(path, 'chatLog.txt')
    if os.path.exists(log_path):
        os.remove(log_path)

def roundUp(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def tokenise(input):
    tokenise = jieba.cut(input, cut_all=True)
    segmented = "/".join(tokenise)
    inputSplit = segmented.split("/")
    inputSplit = list(set(inputSplit))

    return inputSplit

def retrieveCategories():
    conn = sqlite3.connect(DBpath)
    cursor = conn.cursor() 

    cursor.execute('SELECT CategoryID, CategoryName from Categories')
    categories = cursor.fetchall()
    cursor.close()

    return categories

def retrieveOriginalQes(category):
    conn = sqlite3.connect(DBpath)
    cursor = conn.cursor() 

    code = ('SELECT ALL QuestionText from OriginalQuestions WHERE Category = {id}').format(id = category)
    cursor.execute(code)
    questions = cursor.fetchall()
    cursor.close()

    randIndex = random.randint(0, len(questions)-1)
    return questions[randIndex][0]

def retrieveFollowup(categorySelection):
    conn = sqlite3.connect(DBpath)
    cursor = conn.cursor()

    code = ('SELECT QuestionText from FollowupQuestions WHERE Category = {id}').format(id = categorySelection)
    cursor.execute(code)
    followupQuestions = cursor.fetchall()
    cursor.close()

    return followupQuestions

def followupRelevancy(userInput, category):
    tokenisedInp = tokenise(userInput)
    followupQes = retrieveFollowup(category)
    relevancyScoreArray = []
   
    i = 0
    while i < len(followupQes):
        tokenisedQes = tokenise(followupQes[i][0])
        relevancyCount = 0
       
        l = 0
        while l < len(tokenisedQes):
           
            j = 0
            while j < len(tokenisedInp):
                if tokenisedInp[j] == tokenisedQes[l]:
                    relevancyCount = relevancyCount + 1
                j = j + 1

            l = l + 1
        relevancyScore = relevancyCount/len(tokenisedInp)
        relevancyScoreArray.append(roundUp(relevancyScore, 3))

        print("The relevancy score for array index", i, "is:", relevancyScore)
        i = i + 1

    return relevancyScoreArray

def followupApproximation(userInput, category):
    relevancyArray = followupRelevancy(userInput, category)
    followupQes = retrieveFollowup(category)

    maxRelevancy = max(relevancyArray)
    i = 0
    while i < len(relevancyArray)-1:
        if (maxRelevancy == relevancyArray[i]):
            break
        i = i + 1

    print(followupQes[i][0], "    RS(", relevancyArray[i],")")
    return followupQes[i][0]

def createLog(input_type, input):
    now = datetime.now()
    current_time = now.strftime("%H:%M")

    with open(txt_path, 'a', encoding="utf_8") as file:
        if input_type == "user":
            text = (" (" + current_time + ") | " + "\U0001F464" + ": " + input)
            file.write('\n')
            file.write(text)
        elif input_type == "bot":
            text = (" (" + current_time + ") | " + "\U0001F916" + ": " + input)
            file.write('\n')
            file.write(text)
    
    return text

def read_Log():
    text_file = io.open(txt_path, mode="r", encoding="utf-8")
    log_text = text_file.read()
    text_file.close()

    return log_text
