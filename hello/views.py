from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest
from .models import Greeting
from termcolor import colored
import requests
import os

n = 3
# initialize board to have all spaces and be n by n
board = [[' ']*n for x in xrange(n)]
ourPlayer = 'o'

def isBoardStringValid(boardString):
    # board must be exactly 9 characters
    if len(boardString) != 9:
        print "board string is incorrect length"
        return False

    num_x = 0
    num_o = 0
    print "boardString is [" + boardString + "]"
    for c in boardString:
        if c not in 'xo ':
            print "found an invalid character [" + c + "]"
            return False
        if c == 'x':
            num_x += 1
        if c == 'o':
            num_o += 1

    oWentFirst = (num_o == num_x)
    xWentFirst = (num_o == (num_x - 1))
    if not (oWentFirst or xWentFirst):
        print "o or x did not go first"
        return False
    return True

def createBoard(boardString):
    for i in range(n):
        for j in range(n):
            board[i][j] = boardString[i*n+j]

def winningBoard(boardArray):
    # check to see if someone won vertically
    for j in range(n):
        if boardArray[0][j] == boardArray[1][j] and boardArray[1][j] == boardArray[2][j]:
            print boardArray[0][j] + " won in a column"
            return boardArray[0][j]

    # check to see if someone one horizontally
    for i in range(n):
        if boardArray[i][0] == boardArray[i][1] and boardArray[i][1] == boardArray[i][2]:
            print boardArray[i][0] + " won in a row"
            return boardArray[i][0]

    # check to see if someone won on a diagonal
    if boardArray[0][0] == boardArray[1][1] and boardArray[1][1] == boardArray[2][2]:
        print boardArray[0][0] + " won on a diagonal"
        return boardArray[0][0]
    if boardArray[0][2] == boardArray[1][1] and boardArray[1][1] == boardArray[2][0]:
        print boardArray[0][2] + " won on a diagonal"
        return boardArray[0][2]
    return ''

def movesLeft(boardArray):
    for i in range(n):
        for j in range(n):
            if boardArray[i][j] == ' ':
                return True
    return False

def initBoard(boardString):
    # make sure the string passed in is valid
    if False == isBoardStringValid(boardString):
        return False;

    createBoard(boardString)
    printBoard(board)

    # check to see if someone already won
    if winningBoard(board) != '':
        return False
    
    # check to see if there are any moves left
    if False == movesLeft(board):
        return HttpResponseBadRequest()

    # Run our unit tests
    testIsBoardStringValid()
    testWinningBoard()
    testMovesLeft()
    return True

def nextMove(boardArray):
    for i in range(n):
        for j in range(n):
            if boardArray[i][j] == ' ':
                boardArray[i][j] = 'o'
                print "found a blank spot"
                return convertBoardToString(boardArray)
    return convertBoardToString(boardArray)

def convertBoardToString(boardArray):
    retString = ''
    print boardArray
    print "retString: [" + retString + "]"
    for i in range(3):
        print "retString: [" + retString + "]"
        print boardArray[i][0:3]
        retString += ''.join(boardArray[i][0:3])
    return retString
        
# Create your views here.
def index(request):
    boardString = request.GET.get('board')
    print "boardString is [" + boardString + "]"
    if False == initBoard(boardString):
        return HttpResponseBadRequest()

    newBoardString = nextMove(board)
    return HttpResponse(newBoardString)

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, 'db.html', {'greetings': greetings})

##########################
# Debugging methods
##########################
def printBoard(board):
    printFriendlyBoard = [['_']*n for x in xrange(n)]
    for i in range(n):
        for j in range(n):
            if board[i][j] != ' ':
                printFriendlyBoard[i][j] = board[i][j]
    for i in range(n):
        print ''.join(printFriendlyBoard[0:n][i])

##########################
# Testcases
##########################
def testIsBoardStringValid():
    testPrefix = "Test board input"
    # too long
    boardString = " xxo  o   "
    validBoard = isBoardStringValid(boardString)
    test(testPrefix + " is too long", validBoard == False)
    # too short
    boardString = " xxo  o "
    validBoard = isBoardStringValid(boardString)
    test(testPrefix + " is too short", validBoard == False)
    # just right
    boardString = " xxo  o  "
    validBoard = isBoardStringValid(boardString)
    test(testPrefix + " is just the right length", validBoard == True)
    #invalid character
    boardString = " xxo  oj "
    validBoard = isBoardStringValid(boardString)
    test(testPrefix + " has an invalid character", validBoard == False)
    #too many o's
    boardString = " xxo  oo "
    validBoard = isBoardStringValid(boardString)
    test(testPrefix + " has too many o's.. can't possibly be o's turn", validBoard == False)
    #too many x's
    boardString = " xxx  ox "
    validBoard = isBoardStringValid(boardString)
    test(testPrefix + " has too many x's.. can't possibly be o's turn", validBoard == False)

def testWinningBoard():
    #x won horizontally
    boardArray = [['x', 'x', 'x'], [' ',' ','o'], ['o',' ','o']] 
    winner = winningBoard(boardArray)
    test ("x won on a horizontal row", winner == 'x')
    #o won horizontally
    boardArray = [['o', 'o', 'o'], [' ',' ','x'], ['x',' ','x']] 
    winner = winningBoard(boardArray)
    test ("o won on a horizontal row", winner == 'o')
    #x won vertically
    boardArray = [['x', 'o', 'o'], ['x',' ','o'], ['x',' ','o']] 
    winner = winningBoard(boardArray)
    test ("x won on a vertical row", winner == 'x')
    #o won vertically
    boardArray = [['o', ' ', 'o'], ['o',' ','x'], ['o',' ','x']] 
    winner = winningBoard(boardArray)
    test ("o won on a vertical row", winner == 'o')
    #x won on a diagonal 
    boardArray = [['x', 'o', 'o'], [' ','x','o'], [' ',' ','x']] 
    winner = winningBoard(boardArray)
    test ("x won on a diagonal", winner == 'x')
    #o won on a diagonal 
    boardArray = [['o', ' ', 'x'], [' ','o','x'], ['x',' ','o']] 
    winner = winningBoard(boardArray)
    test ("o won on a diagonal", winner == 'o')
    #x won on a diagonal 
    boardArray = [[' ', 'o', 'x'], [' ','x','o'], ['x',' ','o']] 
    winner = winningBoard(boardArray)
    test ("x won on a diagonal", winner == 'x')
    #o won on a diagonal 
    boardArray = [['x', ' ', 'o'], [' ','o','x'], ['o',' ','x']] 
    winner = winningBoard(boardArray)
    test ("o won on a diagonal", winner == 'o')

def testMovesLeft():
    boardArray = [['x', 'x', 'o'], ['x','o','x'], ['o','o','x']] 
    test ("There are no moves left", movesLeft(boardArray) == False)
    boardArray = [['x', ' ', 'o'], ['x','o','x'], ['o','o','x']] 
    test ("There are moves left", movesLeft(boardArray))
    

def test(testName, testPassed):
    if testPassed:
        output = 'PASSED: ' + testName
        print colored(output, 'green')
    else:
        output = 'FAILED: ' + testName
        print colored(output, 'red')

