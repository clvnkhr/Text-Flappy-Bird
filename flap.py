#flap.py
#Calvin Khor
#First game ever!
#learned how to use curses, sort with basic lambda function key

import copy as cp
import time, math, random, curses

def newCol(): #make the next column that will appear   #height should be the height of the game screen
    newColumn = ['*' for _ in range(height)]
    x = random.randint(1,height-1 -1 ) #make the center of the hole of the column (-1 for off-by-one error, -1 so that holes are always size 3 )
    for i in [x-1,x,x+1]:
        newColumn[i] = ' '  #make the hole
    return newColumn

def advance(aList,elt): #remove first element of a list and append elt to end
    temp = cp.deepcopy(aList[1:])
    temp.extend(elt)
    #print('1' + ''.join(aList) + '\n2' + ''.join(temp))
    return cp.deepcopy(temp)

def updateBoard(board, empty=True):
    output = []
    newColumn = newCol()
    
    for t,line in enumerate(board):
        if empty:
            output.append(advance(line,' '))
        else:
            output.append(advance(line,newColumn[t]))

    return cp.deepcopy(output)

def birdPos(x0, t):
    return int(math.floor( x0  - 0.08*(5*5) + 0.08*(t-5)*(t-3) )) #formula chosen empirically

def bird(width):
    return width//10

def collided(pos,board):
    return (pos < 0 or pos > height-1 or '*' == board[pos][bird(width)])

def centerText(screen, height, string):
    _,swidth = screen.getmaxyx()
    screen.addstr(height, (swidth - len(string))//2 , string)

def play(screen,height,width,player,highScorer):
    board = [ [ ' ' for _ in range(width)] for _ in range(height)]

    time.sleep(0.5)
    pillarDist = width//4
    border = ''.join('-' for _ in range(width))
    button = 0 #'ord' of button pressed

    timer = 0 #time elapsed, used to count score
    t = 0 #time in air since last jump

    x0 = height//2 #beginning bird position
    collisionFlag = False
    scores = []

    while button != ord('q') and False == collisionFlag :
        screen.clear()
        newBoard = updateBoard(board, (0!=timer%pillarDist) )
        board = cp.deepcopy(newBoard)
        counter = 0
        for line in board:
            screen.addstr(counter, 0, ''.join(line) )
            counter += 1
        #check for collision

        #draw the bird
        if ord(' ') == button:
            x0 = birdPos(x0, t-1)
            t=0
        pos = birdPos(x0, t)
        if collided(pos,board):
            collisionFlag = True
        else: 
            screen.addstr(birdPos(x0, t),bird(width),'@') 

        #draw the UI
        if timer < 25:
            centerText(screen, height//3  , 'press space to jump!')
            centerText(screen, height//3+1, 'press q to exit')

        #screen.addstr(0,0,border)
        screen.addstr(height,0, border)
        score = max([0,(timer+bird(width))//(pillarDist+1) - 3]) #score works empirically...
        if score <= highScorer[1]:
            centerText(screen, height+2,'Name: ' + str(player) + '  ' + 'Score: ' + str(score) + '  ' + 'Highscore: ' + highScorer[0] + ' ' + str(highScorer[1]) )
        else:
            centerText(screen, height+2,'Name: ' + str(player) + '  ' + 'Score: ' + str(score) + '  ' + 'Highscore: ' + player + ' ' + str(score) )
            centerText(screen, height+3,'New Highscore!' )



        screen.refresh()
        time.sleep(0.05)
        button = screen.getch()

        #increment counters
        timer   += 1
        t       += 1

    if True == collisionFlag:
        centerText(screen, screenHeight//2,'You Collided!')
    centerText(screen, screenHeight//2 + 1,'Your Score:' + str(score) )
    screen.refresh()
    time.sleep(1)
    return score


#main program


screen = curses.initscr()

(screenHeight,screenWidth) = screen.getmaxyx()
height = screenHeight - 5
width = screenWidth - 1
scores = []


f = open('scores'+str(height)+'x'+str(width)+'.txt', 'a+')
f.seek(0)
for line in f:
    temp = line.split()
    scores.append( [temp[0], int(temp[1]) ] )

scores.sort(key = lambda x: x[1], reverse = True)
        
f.seek(0)
f.truncate()

player = 'anonymous'

firstRun = True
button = ord('n')
replay = False
while True:
    screen.clear()
    if True == firstRun:
        button = ord('3')
        firstRun = False
    elif True == replay:
        button = ord('1')
        replay = False
    else:
        screen.clear()
        screen.nodelay(0)
        centerText(screen, height//2-2, 'flap.py' )
        centerText(screen, height//2, 'press 1 to play, 2 to see the highscores, 3 to set player name, 4 to quit' )
        button = screen.getch()



    #act on the input
    if ord('1') == button: #play
        screen.nodelay(1)
        if [] == scores:
            scores.append( [player, play( screen,height,width,player,[player, 0]) ] )
        else:
            scores.append( [player, play( screen,height,width,player,scores[0] ) ] )
        scores.sort(key = lambda x: x[1], reverse = True)
        
        button = 0
        while button!= ord('y') and button!= ord('n'):
            centerText(screen, height//2 + 1,'Play again? (y/n)' )
            screen.refresh()
            screen.nodelay(0)
            button = screen.getch()
            if ord('y') == button:
                replay = True
    
    elif ord('2') == button: #display top scores

        screen.clear()
        centerText(screen,2,'Highscores' )
        for i in range( min([height-4,len(scores)]) ):
            screen.addstr(4+i, width //5 , scores[i][0])
            screen.addstr(4+i, width - width//5 - len(str(scores[i][1])) , str(scores[i][1]))
        button = screen.getch()

    elif ord('3') == button: #set player name

        screen.clear()
        playerExistsFlag = 0
        if player not in  ['', '\n', ' ']:
            centerText(screen,3,'Current name: ' + player )
            playerExistsFlag = 1
        centerText(screen,3+playerExistsFlag,'Type your name and press enter: ' )
        
        temp = ''
        while ord('\n') != button:
            button = screen.getch()
            temp += chr(button)
        player = cp.deepcopy(temp[:-1])


    elif ord('4') == button: #quit

        #save scores
        for line in scores:
            f.write(line[0] + ' ' + str(line[1]) + '\n')
        f.close()
        break

curses.endwin()
    
