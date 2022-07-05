from re import X
from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"a", "e", "i", "o", "u"}
roundstatus = ""
finalroundtext = ""


def readDictionaryFile():
    global dictionary
    # Read dictionary file in from dictionary file location
    # Store each word in a list.
    d = open(dictionaryloc)
    words = d.read()
    d.close()
    dictionary = words.split("\n")
      
    
def readTurnTxtFile():
    global turntext   
    #read in turn intial turn status "message" from file
    t = open(turntextloc)
    turntext = t.read()
    t.close()

        
def readFinalRoundTxtFile():
    global finalroundtext   
    #read in turn intial turn status "message" from file
    f = open(finalRoundTextLoc)
    finalroundtext = f.read()
    f.close

def readRoundStatusTxtFile():
    global roundstatus
    # read the round status  the Config roundstatusloc file location 
    r = open(roundstatusloc)
    roundstatus = r.read()
    r.close()

def readWheelTxtFile():
    global wheellist
    # read the Wheel name from input using the Config wheelloc file location
    w = open(wheeltextloc)
    wheelvals = w.read()
    w.close()
    wheellist = wheelvals.split("\n")
    
def getPlayerInfo():
    global players
    # read in player names from command prompt input
    name0 = input("Enter the name of Player 1:")
    name1 = input("Enter the name of Player 2:")
    name2 = input("Enter the name of Player 3:")
    players[0]["name"] = name0
    players[1]["name"] = name1
    players[2]["name"] = name2


def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
        
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile() 
    
def getWord():
    global dictionary
    global blankWord
    #choose random word from dictionary
    #make a list of the word with underscores instead of letters.
    for word in dictionary:
        blank = ""
        for i in range(len(word)):
            blank += "_"
        blankWord.append(blank)

    randomindex = random.randrange(0,len(dictionary),1)
    roundWord = dictionary[randomindex]
    roundUnderscoreWord = blankWord[randomindex]

    return roundWord,roundUnderscoreWord

def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    # Set round total for each player = 0
    # Return the starting player number (random)
    # Use getWord function to retrieve the word and the underscore word (blankWord)
    for i in range(3):
        players[i]["roundtotal"] = 0

    playernumber = random.randrange(0,3,1)
    initPlayer = playernumber

    roundWord,blankWord = getWord()

    return initPlayer


def spinWheel(playerNum):
    global wheellist
    global players
    global vowels
    # Get random value for wheellist
    # Check for bankrupcy, and take action.
    # Check for loose turn
    # Get amount from wheel if not loose turn or bankruptcy
    # Ask user for letter guess
    # Use guessletter function to see if guess is in word, and return count
    # Change player round total if they guess right.

    wheelnum = random.randrange(0,19,1)
    if wheellist[wheelnum] == "BANKRUPT":
        players[playerNum]["roundtotal"] = 0
        stillinTurn = False
    elif wheellist[wheelnum] == "Lose a Turn":
        stillinTurn = False
    else:
        amount = int(wheellist[wheelnum])
        checking = True
        while checking == True:
            letter = input("Enter your guess:").strip().lower()
            if letter not in vowels:
                goodGuess,count = guessletter(letter,playerNum)
                if goodGuess == True:
                    print(f"There are {count} instances of this letter in the word.")
                    players[playerNum]["roundtotal"] += amount
                    stillinTurn = True
                    checking = False
                elif goodGuess == False:
                    stillinTurn = False
                    checking = False
            else:
                print("Invalid input, try again.")
                checking = True

    return stillinTurn


def guessletter(letter, playerNum): 
    global players
    global blankWord
    global roundWord
    # parameters:  take in a letter guess and player number
    # Change position of found letter in blankWord to the letter instead of underscore 
    # return goodGuess= true if it was a correct guess
    # return count of letters in word. 
    # ensure letter is a consonate.
    count = roundWord.count(letter)
    if count == 0:
        goodGuess = False
    else:
        goodGuess = True
        start = 0
        location = []
        for i in range(count):
            location.append(roundWord.find(letter,start))
            start = roundWord.find(letter,start)+1

        listword = list(blankWord)
        for k in range(len(listword)):
            if k in location:
                listword[k] = letter
            else:
                pass
        blankWord = "".join(listword)
    
    return goodGuess, count

def buyVowel(playerNum):
    global players
    global vowels
    
    # Take in a player number
    # Ensure player has 250 for buying a vowelcost
    # Use guessLetter function to see if the letter is in the file
    # Ensure letter is a vowel
    # If letter is in the file let goodGuess = True
    if players[playerNum]["roundtotal"] < 250:
        print("Not enough money to buy a vowel! Choose another option.")
        stillinTurn = True
    else:
        players[playerNum]["roundtotal"] -= 250
        checking = True
        while checking == True:
            letter = input("Enter your guess:").strip().lower()
            if letter in vowels:
                goodGuess,count = guessletter(letter,playerNum)
                if goodGuess == True:
                    print(f"There are {count} instances of this letter in the word.")
                    stillinTurn = True
                    checking = False
                elif goodGuess == False:
                    stillinTurn = False
                    checking = False
            else:
                print("Invalid input, try again.")
                checking = True


    return stillinTurn     
        
def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    
    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    # Fill in blankList with all letters, instead of underscores if correct 
    # return False ( to indicate the turn will finish)  
    guess = input("Enter your guess:").strip().lower()
    if guess == roundWord:
        players[playerNum]["gametotal"] = players[playerNum]["roundtotal"]
        blankWord = roundWord
    else:
        print("Incorrect guess!")
    
    return False
    
    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players

    # take in a player number. 
    # use the string.format method to output your status for the round
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    
    stillinTurn = True
    while stillinTurn:
        
        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word
        print(turntext.format())
        choice = input("Enter 'S' to spin the wheel, 'B' to buy a vowel, or 'G' to guess the word:")
                
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            stillinTurn = buyVowel(playerNum)
        elif(choice.strip().upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")        
    if blankWord == roundWord:
        return False
    else:
        return True
    
    # Check to see if the word is solved, and return false if it is,
    # Or otherwise break the while loop of the turn.     


def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    initPlayer = wofRoundSetup()
    
    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
        # Use the wofTurn fuction to dive into each players turn until their turn is done.
    progress = True
    nextplayer = initPlayer
    while progress == True:
        if nextplayer > 2:
            nextplayer = 0
            progress = wofTurn(nextplayer)
            nextplayer += 1
        else:
            progress = wofTurn(nextplayer)
            nextplayer += 1

    roundstatus.format()
    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.

def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    winplayer = 0
    amount = 0
    
    # Find highest gametotal player.  They are playing.
    # Print out instructions for that player and who the player is.
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    # Print out the current blankWord again
    # Remember guessletter should fill in the letters with the positions in blankWord
    # Get user to guess word
    # If they do, add finalprize and gametotal and print out that the player won 


def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound()
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()
    
    
