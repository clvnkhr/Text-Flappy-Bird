import curses,time

screen = curses.initscr()
n=1
while n<10:
	screen.clear()
	screen.addstr(n, n, ''.join(['Hello','World']))
	screen.refresh()
	time.sleep(0.1)
	n+=1

screen.refresh()
screen.getch()
curses.endwin()
