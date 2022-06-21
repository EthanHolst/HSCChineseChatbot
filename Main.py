import jieba # library for tokenisation/segmentation of string of Chinese characters
import sqlite3 # library for connecting python code to the database of accounts/questions
import math # library for rounding relevancy scores of database questions for the chatbot
import random # library for selecting a random initial question for the chatbot 
import os # library for establishing paths for the chat log and database
import io # library for opening and reading textfile with utf-8 encoding, allowing for interpretation of Chinese characters
from datetime import datetime # library for the current date, day and time for logging user and bot chat time

# sets path as the folder this python file is in and then finds the accounts/questions database from that
path = os.path.dirname(os.path.abspath(__file__))
DBpath = os.path.join(path, 'QuestionDatabase.db')

# sets path as the folder this python file is in and then finds the chat log text file from that
txt_path = os.path.join(path, 'chatLog.txt')

# function that deletes the log book file on startup of the chatbot function, allowing for the log to be reset
def clear_existing_log():
    log_path = os.path.join(path, 'chatLog.txt')
    if os.path.exists(log_path):
        os.remove(log_path)

# function that is used to round the relevancy scores for chatbot questions for the user input, rounds to 3 decimal places
def roundUp(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

# takes the input and runs it into the Jieba library to tokenise the string into the highest and smallest possible words in the string, 
# which allows for higher accuracy with a bit extra processing time. It then returns the segmented string as a list 
def tokenise(input):
    tokenise = jieba.cut(input, cut_all=True)
    segmented = "/".join(tokenise)
    inputSplit = segmented.split("/")
    inputSplit = list(set(inputSplit))

    return inputSplit

# connects to the database through the cursor, selecting and reading the CategoryID and CategoryName from the Category table, and returns it
def retrieveCategories():
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor() 

    cursor.execute('SELECT CategoryID, CategoryName from Categories')
    categories = cursor.fetchall()
    cursor.close()

    return categories

# with a passed in category, the function selects the relevant QuestionText(s) from the OriginalQuestion database and then returns a random initial question
# from that category
def retrieveOriginalQes(category):
    connect = sqlite3.connect(DBpath)
    cursor = connect.cursor() 

    code = ('SELECT ALL QuestionText from OriginalQuestions WHERE Category = {id}').format(id = category)
    cursor.execute(code)
    questions = cursor.fetchall()
    cursor.close()

    randIndex = random.randint(0, len(questions)-1)
    return questions[randIndex][0]

# with a passed in category, the function selects the relevant QuestionText(s) from the FollowupQuestion database and then returns an array of all the followup
# questions in that category
def retrieveFollowup(category):
    conn = sqlite3.connect(DBpath)
    cursor = conn.cursor()

    code = ('SELECT QuestionText from FollowupQuestions WHERE Category = {id}').format(id = category)
    cursor.execute(code)
    followupQuestions = cursor.fetchall()
    cursor.close()

    return followupQuestions

# 1. the function takes the category the chatbot has began in and the current user input to find the most appropriate response in the database
# 2. it runs the tokenise() and retrieveFollowup() functions to get the tokenised input and all followup questions of the selected category
# 3. it then loops through the applicable tokenised form followup questions in comparison to the tokenised input whilst counting the amount of
#    similar tokens
# 4. it then calculates a score by diving the sum of similar tokens by the amount of tokens in the input to find the percentage of similarity
#    between the responses to estimate the most appropriate followup
# 5. these scores are then appended to an array and returned
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

# function takes the array of followup relevancy from followupRelevancy() and returns the highest relevancy followup question, which is a string of Chinese characters,
# as well as printing all the followup questions with their relevancy in the terminal
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

# with a passed in input_type, which can be user or bot, and input, the function writes a log to the chatlog.txt file with a differnet emoji for users to represent
# the user type and it also contains the current time that the input was added, for teacher reference
# it opens the text file to write with utf-8 so that Chinese characters can be written on the document
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

# the function reads the chatLog file with utf-8 encoding to interpret the Chinese unicode and then returns this string of the chatLog
def read_Log():
    text_file = io.open(txt_path, mode="r", encoding="utf-8")
    log_text = text_file.read()
    text_file.close()

    return log_text
