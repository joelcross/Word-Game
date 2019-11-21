'''
This program runs a word game.

Author: Joel Cross
Date: Oct. 5, 2018
'''

import string
import random
import urllib.request

# Load the wordlist from the URL into a list named "data" and returns the list
def readWordList():
    response = urllib.request.urlopen("http://www.mit.edu/~ecprice/wordlist.10000")
    html = response.read()
    data = html.decode('utf-8').split()

    return data


# Removes all words comprised of one repeated letter from the word list and returns data for use in the test function
def cleanseList(data):
    # Go through each word in list
    for element in data:
        # Don't check for words which are only 1 letter long
        if len(element) > 1:
            firstLetter = element[0]
            # Search through each letter in word
            for x in range (len(element)):
                # If any letter different from the first is found at any spot in the word
                if firstLetter != element[x]:
                    badWord = False
                # If the entire word is the same letter
                else:
                    badWord = True
            if badWord == True:
                data[data.index(element)] = 1 # Replace all single-letter words with a placeholder "1"

    # Switching the data to a set and back to a list removes all duplicates (in this case, the 1's)
    data = set(data)
    data = list(data)

    for element in data:
        # If any words of all the same letter were found in the list, a 1 will now be in the first position of the list. We must remove it.
        if data[0] == 1:
            del data[0]

    return data
            

# Generate and return two random letters
def generateLetters():
    letter1 = random.choice(string.ascii_lowercase)
    letter2 = random.choice(string.ascii_lowercase)

    return letter1, letter2


# Prompts the user to enter a word and then returns this word
def enterWord(data, letter1, letter2):
    word = input("Enter a word beginning with " + letter1 + " and ending with " + letter2 + ": ")
    word = word.lower()

    return word


# Calculates how many points the user will recieve for the word they entered. Returns this score.
def scoring(enteredWord, firstLetter, secondLetter, wordList, totalScore):
    letterValues = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 1, 'f': 5, 'g': 2, 'h': 3, 'i': 1,
                     'j': 9, 'k': 5, 'l': 1, 'm': 2, 'n': 2, 'o': 1, 'p': 4, 'q': 15, 'r': 1,
                     's': 1, 't': 1, 'u': 1, 'v': 8, 'w': 4, 'x': 15, 'y': 4, 'z': 15 } 
    roundScore = 0
    wordCheck = False
    letterCheck = False
    
    # If the word entered by the user starts and ends with the given letters
    if enteredWord[0] == firstLetter and enteredWord[len(enteredWord)-1] == secondLetter:
        letterCheck = True      
        # Check if the entered word is actually a word
        for element in wordList: # Go through each word in the master list of words
            if enteredWord == element: # If the entered word IS a word
                wordCheck = True
                # Check how many points each letter in word is worth
                for letter in range (len(enteredWord)):
                    if enteredWord[letter] in letterValues:
                        roundScore = roundScore + letterValues[enteredWord[letter]]
                # Check if first and last letters in word are the same (and give bonus points if necessary)
                if firstLetter == secondLetter:
                    roundScore = roundScore + 10
                # Bonus points for longer words
                if len(enteredWord) == 6:
                    roundScore = roundScore + 3
                elif len(enteredWord) == 7:
                    roundScore = roundScore + 4
                elif len(enteredWord) == 8:
                    roundScore = roundScore + 5
                elif len(enteredWord) > 8:
                    roundScore = roundScore + 6
        if wordCheck == False: # The entered word is NOT a word
            roundScore = roundScore-10
    else: # The word entered does not start/end with the correct letters
        roundScore = roundScore - 2

    totalScore = totalScore+roundScore
    print("Round Score: " + str(roundScore))
    print("Total Score: " + str(totalScore))

    return totalScore


# Tests to ensure the cleanseList() function works properly
def test():
    myList = ['a', 'aa', 'b', 'aaaaaa', 'ffff', 'dddddb', 'apple']
    print("List before cleanse:")
    print(myList)
    print("List after cleanse:")
    print(cleanseList(myList))


# Runs the game by making use of other functions
def gameplay():
    # Read and cleanse the word list
    data = readWordList()
    cleanseList(readWordList())

    # Initialize the totalScore and roundNum variables
    totalScore = 0
    roundNum = 1

    # Round begins
    while roundNum != 6: # Run game for max of 5 rounds
        print("\nRound " + (str(roundNum)) + ":")
        letter1, letter2 = generateLetters()
        word = enterWord(readWordList(), letter1, letter2)
        totalScore = scoring(word, letter1, letter2, data, totalScore)

        while True:
            if roundNum == 5: # If it is the final round, end the game
                print("Thanks for playing! Your final score is " + str(totalScore) + " points.")
                exit()

            # After each round, ask the user if they would like to continue playing
            answer = input("Would you like to keep playing? Type yes/no: ")
            while answer.lower() not in ("yes","no"): # Continue to ask unitl they give a valid answer
                answer = input("Would you like to keep playing? Type yes/no: ")
            if answer == "yes": # If they want to keep playing, start a new round
                roundNum = roundNum+1
                break
            if answer == "no": # If they want to quit, the program closes
                exit()
            
            
gameplay()
