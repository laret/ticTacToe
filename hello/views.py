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


# Create your views here.
def index(request):
    boardString = request.GET.get('board')
    print "boardString is [" + boardString + "]"
    if isBoardStringValid(boardString) == False:
        return HttpResponseBadRequest()

    testIsBoardStringValid()

    createBoard(boardString)
    print board
    print boardString
    printBoard(board)    
    return HttpResponse(boardString)

    #times = int(os.environ.get('TIMES',3))
    #return HttpResponse(board * times)
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

def test(testName, testPassed):
    if testPassed:
        output = 'PASSED: ' + testName
        print colored(output, 'green')
    else:
        output = 'FAILED: ' + testName
        print colored(output, 'red')

