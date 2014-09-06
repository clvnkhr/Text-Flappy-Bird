import copy as cp
import time
import random

width = 50 
height = 20 #for NewCol to work, need height at least 3.
screen = [ [ ' ' for _ in range(width)] for _ in range(height)]
runTime = 1000
border = '\n' + ''.join('_' for _ in range(width)) + '\n'
bigEmptySpace = ''.join('\n' for _ in range(100)) #hacky 'clear terminal'


def drawBird(screen,position = (height//2,width//10)):
    screen[ position[0] ][ position[1] ] = '@'

def printScreen(screen):
    temp = cp.deepcopy(screen)
    drawBird(temp)
    print(bigEmptySpace + border + '\n'.join([''.join(line) for line in temp]) + border )

def newCol(): #make the next column that will appear
    if False:
        return [' ' for _ in range(height)]
    else:
        newColumn = ['*' for _ in range(height)]
        x = random.randint(1,height-1 -1 )
        for i in [x-1,x,x+1]:
            newColumn[i] = '.'
        return newColumn

def advance(aList,elt): #remove first element of a list and append elt to end
    temp = cp.deepcopy(aList[1:])
    temp.extend(elt)
    #print('1' + ''.join(aList) + '\n2' + ''.join(temp))
    return cp.deepcopy(temp)

def updateScreen(screen, empty=True):
    output = []
    newColumn = newCol()
    t = 0
    for line in screen:
        if empty:
            output.append(advance(line,' '))
        else:
            output.append(advance(line,newColumn[t]))
        t=t+1
    return cp.deepcopy(output)

    
#Main Program
for n in range(runTime):
    screen = updateScreen(screen,(0!=n%10))
    printScreen(screen)
    time.sleep(0.08)
    
    
