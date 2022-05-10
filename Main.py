import jieba
import math
import sqlite3
import os

path = os.path.dirname(os.path.abspath(__file__))
DBpath = os.path.join(path, 'QuestionDatabase.db')

stubInput = "我有很多好的学校课，我很喜欢我的老师们。"

def roundUp(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def tokenise(input):
    tokenise = jieba.cut(input, cut_all=True)
    segmented = "/".join(tokenise)
    inputSplit = segmented.split("/")
    inputSplit = list(set(inputSplit))

    return inputSplit

def retrieveFollowup(categorySelection):
    conn = sqlite3.connect(DBpath)
    cursor = conn.cursor()

    code = ('SELECT QuestionText from FollowupQuestions WHERE Category = {id}').format(id = categorySelection)
    cursor.execute(code)
    followupQuestions = cursor.fetchall()
    cursor.close()

    return followupQuestions


def retrieveCategories():
    conn = sqlite3.connect(DBpath)
    cursor = conn.cursor() 

    cursor.execute('SELECT CategoryID, CategoryName from Categories')
    categories = cursor.fetchall()
    cursor.close()

    return categories


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
    maxRelevancy = max(relevancyArray)
    i = 0
    while i < len(relevancyArray):
        if (maxRelevancy == relevancyArray[i]):
            break

        i = i + 1
        
    followupQes = retrieveFollowup(category)
    print(followupQes[i][0], "Is the most accurate followup with a score of", relevancyArray[i])

followupApproximation(stubInput, 1)

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




# if using synonyms: https://github.com/chatopera/Synonyms
# Potential Things to be added:
# 1. Takes a database of replies to a certain question that teachers can select as appropriate or not, which is then used to score the user responses based off keywords, length etc. 
#    Can also send this feedback to the user that wrote the repsponse for the reason it was selected as inappropriate
# 2. Sorts the responses in text files/ other appropriate databases by keywords and original questions, making the search for comparable texts more resource efficient and quick