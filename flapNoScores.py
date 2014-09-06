import copy as cp
import time, math, random, curses

def newCol(): #make the next column that will appear
    newColumn = ['*' for _ in range(height)]
    x = random.randint(1,height-1 -1 )
    for i in [x-1,x,x+1]:
        newColumn[i] = ' '
    return newColumn

def advance(aList,elt): #remove first element of a list and append elt to end
    temp = cp.deepcopy(aList[1:])
    temp.extend(elt)
    #print('1' + ''.join(aList) + '\n2' + ''.join(temp))
    return cp.deepcopy(temp)

def updateBoard(board, empty=True):
    output = []
    newColumn = newCol()
    t = 0
    for line in board:
        if empty:
            output.append(advance(line,' '))
        else:
            output.append(advance(line,newColumn[t]))
        t=t+1
    return cp.deepcopy(output)

def birdPos(x0, t):
    return int(math.floor( x0  - 0.08*(5*5) + 0.08*(t-5)*(t-3) ))
def bird(width):
    return width//10

def collided(pos,board):
    return (pos < 0 or pos > height-1 or '*' == board[pos][bird(width)])

def centerText(screen, height, string):
    (_,swidth) = screen.getmaxyx()
    screen.addstr(height, (swidth - len(string))//2 , string)



#main program

screen = curses.initscr()
screen.nodelay(1)

(screenHeight,screenWidth) = screen.getmaxyx()
height = screenHeight - 5
width = screenWidth - 1

def play(screen,height,width):
    board = [ [ ' ' for _ in range(width)] for _ in range(height)]

    time.sleep(0.5)
    pillarDist = width//4
    border = ''.join('-' for _ in range(width))
    key = 0 #'ord' of key pressed

    timer = 0 #time elapsed
    t = 0 #time in air since last jump

    x0 = height//2 #beginning bird position
    collisionFlag = False

    while key != ord('q') and False == collisionFlag :
        screen.clear()
        newBoard = updateBoard(board, (0!=timer%pillarDist) )
        board = cp.deepcopy(newBoard)
        counter = 0
        for line in board:
            screen.addstr(counter, 0, ''.join(line) )
            counter += 1
        #check for collision

        #draw the bird
        if ord(' ') == key:
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
        centerText(screen, height+1,'Score: ' + str(score) )


        screen.refresh()
        time.sleep(0.05)
        key = screen.getch()

        #increment counters
        timer   += 1
        t       += 1

    if True == collisionFlag:
        centerText(screen, screenHeight//2,'You Collided!')
    centerText(screen, screenHeight//2 + 1,'Your Score:' + str(score) )
    screen.refresh()
    time.sleep(1)
    

key = ord('n')
while True:
    if ord('y') == key:
        key = ord('1')
    else:
        screen.clear()
        screen.nodelay(0)
        centerText(screen, height//2-2, 'flap.py' )
        centerText(screen, height//2, 'press 1 to play, 2 to quit' )
        key = screen.getch()
    if ord('1') == key:
        screen.nodelay(1)
        play(screen,height,width)
        screen.clear()
        key = 0
        while key!= ord('y') and key!= ord('n'):
            centerText(screen, height//2 + 1,'Play again? (y/n)' )
            screen.refresh()
            screen.nodelay(0)
            key = screen.getch()
    elif ord('2') == key:
        break

curses.endwin()
    
