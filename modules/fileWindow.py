import time
# file window covers everything about a file and seeing it visually
# filecursor (current location in file), viewport? (what YOU're seeing), screenCursor (wherever you are has to visible _somehow_).

def keepWindowInMainScreen(H,W,Y,X,Window):
	offscreenY = 0
	offscreenX = 0
	offscreen = False
	windowAltered = False

	# if actual window does not fit in main screen

	if standardscreen.getmaxyx()[0] <= Window.getmaxyx()[0] + Window.getbegyx()[0]:	# if screen size x does not fit the window x
		offscreen = True
		offscreenY = Window.getbegyx()[0]+Window.getmaxyx()[0]-standardscreen.getmaxyx()[0]
		if Window.getbegyx()[0]-offscreenY < 0:
			Window.resize(Window.getmaxyx()[0]+(Window.getbegyx()[0]-offscreenY),Window.getmaxyx()[1])
			windowAltered = True
			offscreenY = Window.getbegyx()[0]+Window.getmaxyx()[0]-standardscreen.getmaxyx()[0]
	if standardscreen.getmaxyx()[1] <= Window.getmaxyx()[1] + Window.getbegyx()[1]:
		offscreen = True
		offscreenX = Window.getbegyx()[1]+Window.getmaxyx()[1]-standardscreen.getmaxyx()[1]
		if Window.getbegyx()[1]-offscreenX < 0:
			Window.resize(Window.getmaxyx()[0],Window.getmaxyx()[1]+(Window.getbegyx()[1]-offscreenX))
			windowAltered = True
			offscreenX = Window.getbegyx()[1]+Window.getmaxyx()[1]-standardscreen.getmaxyx()[1]
	if offscreen:
		Window.mvwin(Window.getbegyx()[0]-offscreenY,Window.getbegyx()[1]-offscreenX)
		windowAltered = True
	if standardscreen.getmaxyx()[0] == Window.getmaxyx()[0]:
		if Window.getmaxyx()[0]-1 <= 0:
			Window.resize(1,Window.getmaxyx()[1])
		else:
			Window.resize(Window.getmaxyx()[0]-1,Window.getmaxyx()[1])
		windowAltered = True
	if standardscreen.getmaxyx()[1] == Window.getmaxyx()[1]:
		if Window.getmaxyx()[1]-1 <= 0:
			Window.resize(Window.getmaxyx()[0], 1)
		else:
			Window.resize(Window.getmaxyx()[0], Window.getmaxyx()[1]-1)
		windowAltered = True

	# if there is space available to resize window closer to intended dimensions

	if H > Window.getmaxyx()[0] and standardscreen.getmaxyx()[0] > Window.getmaxyx()[0]+Window.getbegyx()[0]:
		Window.resize(Window.getmaxyx()[0]+(standardscreen.getmaxyx()[0]-Window.getmaxyx()[0]),Window.getmaxyx()[1])
		windowAltered = True
	if Window.getmaxyx()[0] > H:
		if H <= 0:
			H = 1
		Window.resize(H,Window.getmaxyx()[1])
		windowAltered = True
	if W > Window.getmaxyx()[1] and standardscreen.getmaxyx()[1] > Window.getmaxyx()[1]+Window.getbegyx()[1]:
		Window.resize(Window.getmaxyx()[0],Window.getmaxyx()[1]+(standardscreen.getmaxyx()[1]-Window.getmaxyx()[1]))
		windowAltered = True
	if Window.getmaxyx()[1] > W:
		if W <= 0:
			W = 1
		Window.resize(Window.getmaxyx()[0],W)
		windowAltered = True

	# if window can be moved closer to intended position

	if Y > Window.getbegyx()[0] and standardscreen.getmaxyx()[0] > Window.getmaxyx()[0]:
		if standardscreen.getmaxyx()[0] > Y+Window.getmaxyx()[0]:
			Window.mvwin(Y,Window.getbegyx()[1])
			windowAltered = True
		elif Y+Window.getmaxyx()[0] > standardscreen.getmaxyx()[0]:
			Window.mvwin(standardscreen.getmaxyx()[0]-Window.getmaxyx()[0],Window.getbegyx()[1])
			windowAltered = True
	if X > Window.getbegyx()[1] and standardscreen.getmaxyx()[1] > Window.getmaxyx()[1]:
		if standardscreen.getmaxyx()[1] > X+Window.getmaxyx()[1]:
			Window.mvwin(Window.getbegyx()[0],X)
			windowAltered = True
			
		elif X+Window.getmaxyx()[1] > standardscreen.getmaxyx()[1]:
			Window.mvwin(Window.getbegyx()[0],standardscreen.getmaxyx()[1]-Window.getmaxyx()[1])
			windowAltered = True
	changeX = Window.getbegyx()[1]
	changeY = Window.getbegyx()[0]
	if X < Window.getbegyx()[1] and X > 0:
		changeX = X
	if Y < Window.getbegyx()[0] and Y > 0:
		changeY = Y
	if changeX != Window.getbegyx()[1] or changeY != Window.getbegyx()[0]:
		Window.mvwin(changeY, changeX)
		windowAltered = True

	if windowAltered:
		standardscreen.erase()

def start(venicGlobals):
	global filewin, viewport, fileLines, filecursor, standardscreen, filename, intendedHeight, intendedWidth, intendedX, intendedY

	standardscreen = venicGlobals["stdscr"]
	filename = venicGlobals["venicFileName"]

	viewport = [0,0]	# x y
	filecursor = [0,0]	# x y
	venicGlobals["viewport"] = viewport

	intendedX = 0
	intendedY = 0
	# intendedWidth = standardscreen.getmaxyx()[1]
	# intendedHeight = standardscreen.getmaxyx()[0]-5
	intendedWidth = 1
	intendedHeight = 1


	filewin = venicGlobals["curses"].newwin(intendedHeight,intendedWidth,intendedY,intendedX)	# (y,x) of size, (y,x) of position

	venicGlobals["filewin"] = filewin

	filewin.erase()
	
	filepanel = venicGlobals["panel"].new_panel(filewin)

	venicGlobals["filepanel"] = filepanel
	filepanel.bottom()

	keepWindowInMainScreen(intendedHeight,intendedWidth,intendedY,intendedX,filewin)

	# create line array
	fileLines = venicGlobals["venicFile"].splitlines()
	# venicGlobals["fileLines"] = fileLines
	# for loop to orient drawing each line to the window? :(
		# we are walking down the screen, we need to keep track of what line we're on
	windowY = 0	# this is solely a number meant to be incremented, unrelated to fileWindowY
	for line in fileLines[viewport[1]:viewport[1]+filewin.getmaxyx()[0]]:
		filewin.addnstr(windowY,0,line.expandtabs(4)[viewport[0]:],filewin.getmaxyx()[1]-1)
		windowY += 1

def forceWindowCheck():
	keepWindowInMainScreen(intendedHeight,intendedWidth,intendedY,intendedX,filewin)

def loop(venicGlobals):
	global tabDiff
	filewin.erase()

	intendedX = len(str(len(fileLines)))+1
	intendedY = 0
	intendedHeight = standardscreen.getmaxyx()[0] - intendedY - 1
	intendedWidth = standardscreen.getmaxyx()[1] - intendedX - 1

	keepWindowInMainScreen(intendedHeight,intendedWidth,intendedY,intendedX,filewin)
	# filewin.box()
	windowY = 0

	for line in fileLines[viewport[1]:viewport[1]+filewin.getmaxyx()[0]]:
		filewin.addnstr(windowY,0,line.expandtabs(4)[viewport[0]:],filewin.getmaxyx()[1]-1)
		windowY += 1

	# filewin.addstr(0,0,str(intendedY))

	if filecursor[1] >= viewport[1] and filecursor[1] <= viewport[1]+filewin.getmaxyx()[0]-1:
		if len(fileLines) == 0:
			fileLines.append("")
		tabDiff = len(fileLines[filecursor[1]][:filecursor[0]].expandtabs(4)) - len(fileLines[filecursor[1]][:filecursor[0]])
		if filecursor[0]-viewport[0]+tabDiff <= filewin.getmaxyx()[1]-2 and filecursor[0]-viewport[0]+tabDiff >= 0:
			filewin.chgat(filecursor[1]-viewport[1],filecursor[0]-viewport[0]+tabDiff,1,venicGlobals["curses"].color_pair(3) | venicGlobals["curses"].A_REVERSE)

def kill(venicGlobals):
	pass

### FUNCTIONS TO BE CALLED EXTERNALLY

def moveViewportDown():
	viewport[1] += 1
def moveViewportUp():
	if viewport[1] > 0:
		viewport[1] -= 1
def moveViewportRight():
	viewport[0] += 1
def moveViewportLeft():
	if viewport[0] > 0:
		viewport[0] -= 1

def moveFilecursorUp():
	if filecursor[1] > 0:
		filecursor[1] -= 1
		if filecursor[0] > len(fileLines[filecursor[1]]):
			if len(fileLines[filecursor[1]]) > 0:
				filecursor[0] = len(fileLines[filecursor[1]])
			elif len(fileLines[filecursor[1]]) == 0:
				filecursor[0] = 0
	while filecursor[1] < viewport[1]:
		moveViewportUp()
	while filecursor[1] > filewin.getmaxyx()[0]+viewport[1]-1:
		moveViewportDown()
	tabDiff = len(fileLines[filecursor[1]][:filecursor[0]].expandtabs(4)) - len(fileLines[filecursor[1]][:filecursor[0]])
	while filecursor[0]-viewport[0]+tabDiff > filewin.getmaxyx()[1]-2:
		moveViewportRight()
	while filecursor[0]-viewport[0]+tabDiff < 0:
		moveViewportLeft()


def moveFilecursorDown():
	if filecursor[1] < len(fileLines)-1:
		filecursor[1] += 1
		if filecursor[0] > len(fileLines[filecursor[1]]):
			if len(fileLines[filecursor[1]]) > 0:
				filecursor[0] = len(fileLines[filecursor[1]])
			elif len(fileLines[filecursor[1]]) == 0:
				filecursor[0] = 0
		while filecursor[1] > filewin.getmaxyx()[0]+viewport[1]-1:
			moveViewportDown()
		while filecursor[1] < viewport[1]:
			moveViewportUp()
	tabDiff = len(fileLines[filecursor[1]][:filecursor[0]].expandtabs(4)) - len(fileLines[filecursor[1]][:filecursor[0]])
	while filecursor[0]-viewport[0]+tabDiff > filewin.getmaxyx()[1]-2:
		moveViewportRight()
	while filecursor[0]-viewport[0]+tabDiff < 0:
		moveViewportLeft()


def moveFilecursorLeft():
	if filecursor[0] > 0:
		filecursor[0] -= 1
	elif filecursor[0] == 0 and filecursor[1] != 0:
		moveFilecursorUp()
		gotoEndOfLine()
	tabDiff = len(fileLines[filecursor[1]][:filecursor[0]].expandtabs(4)) - len(fileLines[filecursor[1]][:filecursor[0]])
	while filecursor[0]-viewport[0]+tabDiff > filewin.getmaxyx()[1]-2:
		moveViewportRight()
	while filecursor[0]-viewport[0]+tabDiff < 0:
		moveViewportLeft()

def moveFilecursorRight():
	if filecursor[0] < len(fileLines[filecursor[1]]):
		filecursor[0] += 1
	elif filecursor[0] == len(fileLines[filecursor[1]]) and filecursor[1] != len(fileLines)-1:
		moveFilecursorDown()
		gotoStartOfLine()
	tabDiff = len(fileLines[filecursor[1]][:filecursor[0]].expandtabs(4)) - len(fileLines[filecursor[1]][:filecursor[0]])
	while filecursor[0]-viewport[0]+tabDiff > filewin.getmaxyx()[1]-2:
		moveViewportRight()
	while filecursor[0]-viewport[0]+tabDiff < 0:
		moveViewportLeft()

def gotoStartOfLine():
	filecursor[0] = 0
	tabDiff = len(fileLines[filecursor[1]][:filecursor[0]].expandtabs(4)) - len(fileLines[filecursor[1]][:filecursor[0]])
	while filecursor[0]-viewport[0]+tabDiff < 0:
		moveViewportLeft()

def gotoEndOfLine():
	filecursor[0] = len(fileLines[filecursor[1]])
	tabDiff = len(fileLines[filecursor[1]][:filecursor[0]].expandtabs(4)) - len(fileLines[filecursor[1]][:filecursor[0]])
	while filecursor[0]-viewport[0]+tabDiff > filewin.getmaxyx()[1]-2:
		moveViewportRight()

def enterTextAtFilecursor(text):
	lineStringLeft = fileLines[filecursor[1]][:filecursor[0]]
	lineStringRight = fileLines[filecursor[1]][filecursor[0]:]
	lineStringLeft += text
	fileLines[filecursor[1]] = lineStringLeft + lineStringRight
	moveFilecursorRight()

def newLineAtFilecursor():
	lineStringLeft = fileLines[filecursor[1]][:filecursor[0]]
	lineStringRight = fileLines[filecursor[1]][filecursor[0]:]
	fileLines[filecursor[1]] = lineStringLeft
	fileLines.insert(filecursor[1]+1,"")
	moveFilecursorDown()
	fileLines[filecursor[1]] = lineStringRight

def backspaceTextAtFilecursor():
	if filecursor[0] == 0:
		if filecursor[1] > 0:
			lineString = fileLines[filecursor[1]]
			fileLines.pop(filecursor[1])
			moveFilecursorUp()
			gotoEndOfLine()
			fileLines[filecursor[1]] += lineString
	else:
		lineStringLeft = fileLines[filecursor[1]][:filecursor[0]-1]
		lineStringRight = fileLines[filecursor[1]][filecursor[0]:]
		fileLines[filecursor[1]] = lineStringLeft+lineStringRight
		moveFilecursorLeft()

	# filewin.mvwin(0,0)

def saveFile():
	file = open(filename,'w')
	fileString = ""
	linesRow = 0
	for line in fileLines:
		fileString += line+"\n"
#	fileString = fileString[:-1]
	file.write(fileString)
	file.close()

def searchForText():
	pass