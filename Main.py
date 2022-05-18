import jieba
import math
import sqlite3
import os
import random

path = os.path.dirname(os.path.abspath(__file__))
DBpath = os.path.join(path, 'QuestionDatabase.db')

def userInput():
    """ Retrieves categories from DB.
    """
    print("")
    print(retrieveCategories())
    Category = input("Please input the CategoryID of what the category question you would like: ") 
    print(retrieveOriginalQes(Category))
    followupApproximation(Category)

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

def followupApproximation(category):
    continueQ = True
    while continueQ == True:
        userInput = input("Please input your response (\"Stop\" to finish): ")
        if (userInput == "stop" or userInput == "STOP" or userInput == "Stop"):
            continueQ = False

        else:
            relevancyArray = followupRelevancy(userInput, category)
            followupQes = retrieveFollowup(category)

            maxRelevancy = max(relevancyArray)
            i = 0
            while i < len(relevancyArray)-1:
                if (maxRelevancy == relevancyArray[i]):
                    break
                i = i + 1

            print(followupQes[i][0], "    RS(", relevancyArray[i],")")
            
""" 
APPLICATION PROGRESSION PLAN
User functionality :
1. choice of what main question to start with
2. give input 
3. retrieve highest possible relevency response for followup questions under that category
4. option to move onto the next main question or back a question, or to retrieve the next most relevant followup question
- checkbox of audio representation or not

Educator functionality :
1. can add followup questions to the database or update tags of existing ones
2. can flag to remove or existing questions
"""
# Fong additions
# validation - capture those errors 
# explore capturing the inputs and questions each session and send a log to the class teacher#

