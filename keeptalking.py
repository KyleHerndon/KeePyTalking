def lastDigitOdd():
    return 'y' in serial

def hasVowel():
    return 'y' in serial2

def hasParallel():
    return 'y' in parallel

num_bat=int(input("Number of batteries: "))
serial=input("Serial number odd? y/n: ")
serial2=input("Serial number has vowel? y/n:")
parallel=input("Is there a parallel port? y/n:")
frk=input("Lit FRK indicator? y/n:")
car=input("Lit CAR indicator? y/n:")

###WIRE###
def cut(n):
    print("Cut wire", n)
    
def wireModule():
    wire=input("r=red b=blue y=yellow w=white k=black \n Your sequence:")
    wire=wire.strip().replace(" ", "").lower()
    wires=list(wire)
    l=len(wires)
    if l == 3 :
        if 'r' not in wires:
            cut(2)
        elif wires[2]=='w':
             cut(3)
        elif wires[0] == 'b' and wires[1] == 'b':
             cut(2)
        else:
             cut(3)
    elif l == 4:
        if wires.count('r')>1 and lastDigitOdd:
            cut(wire.rfind('r')+1)
        elif wires[3]=='y' and 'r' not in wires:
            cut(1)
        elif wires.count('b') == 1:
            cut(1)
        elif wires.count('y') >1:
            cut(1)
        else:
            cut(2)
    elif l == 5:
        if wires[4] == 'k' and lastDigitOdd():
            cut(4)
        elif wires.count('r') == 1 and wires.count('y') > 1:
            cut(1)
        elif wires.count('k') == 0:
            cut(2)
        else:
            cut(1)
    else:
        if wires.count('y') == 0 and lastDigitOdd():
            cut(3)
        elif wires.count('y') == 1 and wires.count('w')>1:
            cut(4)
        elif wire.count('r') == 0:
            cut(6)
        else:
            cut(4)
###END WIRE###
###BUTTON###
def hasIndicator(str):
    boo=input("Is there a "+str+" indicator? y/n").strip().replace(" ", "").lower()
    return boo == 'y'

def pressHold():
    color=input("Press and hold the button. What color is the strip?").strip().replace(" ", "").lower()
    if color == 'b':
        print("Release on a 4")
    elif color == 'y':
        print("Release on a 5")
    else:
        print("Release on a 1")

def buttonModule():
    text=input("button text: ").strip().replace(" ", "").lower()
    color=input("r=red b=blue y=yellow w=white k=black \n Your color: ").strip().replace(" ", "").lower()
    if color == 'b' and text == 'abort':
        pressHold()
    elif num_bat > 1 and text == "detonate":
        print("Immediately release")
    elif color == 'w' and 'y' in car:
        pressHold()
    elif num_bat>2 and 'y' in frk:
        print("Immediately release")
    elif color == 'y':
        pressHold()
    elif color == 'r' and text == 'hold':
        print("Immediately release")
    else:
        pressHold()
###END BUTTON###
###FIRST###
lookUp={"yes":3,"first":2,"display":6,"okay":2,"says":6,"nothing":3,"":5,"blank":4,"no":6,"led":3,"lead":6,"read":4,"red":4,"reed":5,"leed":5,"hold on":6,"you":4,"you are":6,"your":4,"you're":4,"ur":1,"there":6,"they're":5,"their":4,"they are":3,"see":6,"c":2,"cee":6}
table={"READY": "YES, OKAY, WHAT, MIDDLE, LEFT, PRESS, RIGHT, BLANK, READY, NO, FIRST, UHHH, NOTHING, WAIT",
"FIRST": "LEFT, OKAY, YES, MIDDLE, NO, RIGHT, NOTHING, UHHH, WAIT, READY, BLANK, WHAT, PRESS, FIRST",
"NO": "BLANK, UHHH, WAIT, FIRST, WHAT, READY, RIGHT, YES, NOTHING, LEFT, PRESS, OKAY, NO, MIDDLE",
"BLANK": "WAIT, RIGHT, OKAY, MIDDLE, BLANK, PRESS, READY, NOTHING, NO, WHAT, LEFT, UHHH, YES, FIRST",
"NOTHING": "UHHH, RIGHT, OKAY, MIDDLE, YES, BLANK, NO, PRESS, LEFT, WHAT, WAIT, FIRST, NOTHING, READY",
"YES": "OKAY, RIGHT, UHHH, MIDDLE, FIRST, WHAT, PRESS, READY, NOTHING, YES, LEFT, BLANK, NO, WAIT",
"WHAT": "UHHH, WHAT, LEFT, NOTHING, READY, BLANK, MIDDLE, NO, OKAY, FIRST, WAIT, YES, PRESS, RIGHT",
"UHHH": "READY, NOTHING, LEFT, WHAT, OKAY, YES, RIGHT, NO, PRESS, BLANK, UHHH, MIDDLE, WAIT, FIRST",
"LEFT": "RIGHT, LEFT, FIRST, NO, MIDDLE, YES, BLANK, WHAT, UHHH, WAIT, PRESS, READY, OKAY, NOTHING",
"RIGHT": "YES, NOTHING, READY, PRESS, NO, WAIT, WHAT, RIGHT, MIDDLE, LEFT, UHHH, BLANK, OKAY, FIRST",
"MIDDLE": "BLANK, READY, OKAY, WHAT, NOTHING, PRESS, NO, WAIT, LEFT, MIDDLE, RIGHT, FIRST, UHHH, YES",
"OKAY": "MIDDLE, NO, FIRST, YES, UHHH, NOTHING, WAIT, OKAY, LEFT, READY, BLANK, PRESS, WHAT, RIGHT",
"WAIT": "UHHH, NO, BLANK, OKAY, YES, LEFT, FIRST, PRESS, WHAT, WAIT, NOTHING, READY, RIGHT, MIDDLE",
"PRESS": "RIGHT, MIDDLE, YES, READY, PRESS, OKAY, NOTHING, UHHH, BLANK, LEFT, FIRST, WHAT, NO, WAIT",
"YOU": "SURE, YOU ARE, YOUR, YOU'RE, NEXT, UH HUH, UR, HOLD, WHAT?, YOU, UH UH, LIKE, DONE, U",
"YOU ARE": "YOUR, NEXT, LIKE, UH HUH, WHAT?, DONE, UH UH, HOLD, YOU, U, YOU'RE, SURE, UR, YOU ARE",
"YOUR": "UH UH, YOU ARE, UH HUH, YOUR, NEXT, UR, SURE, U, YOU'RE, YOU, WHAT?, HOLD, LIKE, DONE",
"YOU'RE": "YOU, YOU'RE, UR, NEXT, UH UH, YOU ARE, U, YOUR, WHAT?, UH HUH, SURE, DONE, LIKE, HOLD",
"UR": "DONE, U, UR, UH HUH, WHAT?, SURE, YOUR, HOLD, YOU'RE, LIKE, NEXT, UH UH, YOU ARE, YOU",
"U": "UH HUH, SURE, NEXT, WHAT?, YOU'RE, UR, UH UH, DONE, U, YOU, LIKE, HOLD, YOU ARE, YOUR",
"UH HUH": "UH HUH, YOUR, YOU ARE, YOU, DONE, HOLD, UH UH, NEXT, SURE, LIKE, YOU'RE, UR, U, WHAT?",
"UH UH": "UR, U, YOU ARE, YOU'RE, NEXT, UH UH, DONE, YOU, UH HUH, LIKE, YOUR, SURE, HOLD, WHAT?",
"WHAT?": "YOU, HOLD, YOU'RE, YOUR, U, DONE, UH UH, LIKE, YOU ARE, UH HUH, UR, NEXT, WHAT?, SURE",
"DONE": "SURE, UH HUH, NEXT, WHAT?, YOUR, UR, YOU'RE, HOLD, LIKE, YOU, U, YOU ARE, UH UH, DONE",
"NEXT": "WHAT?, UH HUH, UH UH, YOUR, HOLD, SURE, NEXT, LIKE, DONE, YOU ARE, UR, YOU'RE, U, YOU",
"HOLD": "YOU ARE, U, DONE, UH UH, YOU, UR, SURE, WHAT?, YOU'RE, NEXT, HOLD, UH HUH, YOUR, LIKE",
"SURE": "YOU ARE, DONE, LIKE, YOU'RE, YOU, HOLD, UH HUH, UR, SURE, U, WHAT?, NEXT, YOUR, UH UH",
"LIKE": "YOU'RE, NEXT, U, UR, HOLD, DONE, UH UH, WHAT?, UH HUH, YOU, LIKE, SURE, YOU ARE, YOUR"}
pos={1:"upper left", 2:"upper right", 3:"middle left", 4:"middle right", 5:"bottom left", 6:"bottom right"}
def firstModule():
    display=input("The display says?").strip().replace(" ", "").lower()
    word=input("Read the "+ pos[lookUp[display]]).strip().replace(" ", "").upper()
    print(table[word])
    
    boo=input("Repeat? y/n")
    if boo == 'y':
        firstModule()

###END FIRST###
###PASSWORD###
possibleWords="""about after again below could every first found great house large learn never other place plant point right small sound spell still study their there these thing think three water where which world would write"""
def passModule():
    wordsLeft=possibleWords.split()
    characters=list(input("All possible first characters: ").strip().replace(" ", "").lower())
    for word in wordsLeft[:]:
        if word[0] not in characters:
            wordsLeft.remove(word)
    if len(wordsLeft) == 0:
        print("Mistake, try again")
        return
    elif len(wordsLeft) ==1:
        print("The password is",wordsLeft[0])
        return
    characters=list(input("All possible second characters: ").strip().replace(" ", "").lower())
    for word in wordsLeft[:]:
        if word[1] not in characters:
            wordsLeft.remove(word)
    if len(wordsLeft) == 0:
        print("Mistake, try again")
        return
    elif len(wordsLeft) ==1:
        print("The password is",wordsLeft[0])
        return
    characters=list(input("All possible third characters: ").strip().replace(" ", "").lower())
    for word in wordsLeft[:]:
        if word[2] not in characters:
            wordsLeft.remove(word)
    if len(wordsLeft) == 0:
        print("Mistake, try again")
        return
    elif len(wordsLeft) ==1:
        print("The password is",wordsLeft[0])
        return
    characters=list(input("All possible fourth characters: ").strip().replace(" ", "").lower())
    for word in wordsLeft[:]:
        if word[3] not in characters:
            wordsLeft.remove(word)
    if len(wordsLeft) == 0:
        print("Mistake, try again")
        return
    elif len(wordsLeft) ==1:
        print("The password is",wordsLeft[0])
        return
    characters=list(input("All possible fifth characters: ").strip().replace(" ", "").lower())
    for word in wordsLeft[:]:
        if word[4] not in characters:
            wordsLeft.remove(word)
    if len(wordsLeft) ==1:
        print("The password is",wordsLeft[0])
        return
    print("Mistake, try again")
    return
    
###END PASSWORD###
###MEMORY###
def memoryModule():
    print("Input is done as follows: [display number][button numbers from left to right]")
    print("All output is the label of the button you should press")
    positionPressed=[]
    buttonPressed=[]
    ###Stage 1
    data=list(input("Data: ").strip().replace(" ", "").lower())
    if data[0] =='3':
        positionPressed.append(3)
        buttonPressed.append(data[3])
        print("Press",data[3])
    elif data[0] =='4':
        positionPressed.append(4)
        buttonPressed.append(data[4])
        print("Press",data[4])
    else:
        positionPressed.append(2)
        buttonPressed.append(data[2])
        print("Press",data[2])
    ###Stage 2
    data=list(input("Data: ").strip().replace(" ", "").lower())
    if data[0] == '1':
        positionPressed.append(data.index('4'))
        buttonPressed.append('4')
        print("Press 4")
    elif data[0] == '3':
        positionPressed.append(1)
        buttonPressed.append(data[1])
        print("Press",data[1])
    else:
        positionPressed.append(positionPressed[0])
        buttonPressed.append(data[positionPressed[0]])
        print("Press",data[positionPressed[0]])
    ###Stage 3
    data=list(input("Data: ").strip().replace(" ", "").lower())
    if data[0] == '1':
        positionPressed.append(data[1:5].index(buttonPressed[1])+1)
        buttonPressed.append(buttonPressed[1])
        print("Press",buttonPressed[1])
    elif data[0] == '2':
        positionPressed.append(data[1:5].index(buttonPressed[0])+1)
        buttonPressed.append(buttonPressed[0])
        print("Press",buttonPressed[0])
    elif data[0] == '3':
        positionPressed.append(3)
        buttonPressed.append(data[3])
        print("Press",data[3])
    else:
        positionPressed.append(data[1:5].index("4")+1)
        buttonPressed.append("4")
        print("Press 4")
    ###Stage 4
    data=list(input("Data: ").strip().replace(" ", "").lower())
    if data[0] == '1':
        positionPressed.append(positionPressed[0])
        buttonPressed.append(data[positionPressed[0]])
        print("Press",data[positionPressed[0]])
    elif data[0] == '2':
        positionPressed.append(1)
        buttonPressed.append(data[1])
        print("Press",data[1])
    else:
        positionPressed.append(positionPressed[1])
        buttonPressed.append(data[positionPressed[1]])
        print("Press",data[positionPressed[1]])
    ###Stage 5
    data=list(input("Data: ").strip().replace(" ", "").lower())
    if data[0] == '1':
        positionPressed.append(data[1:5].index(buttonPressed[0])+1)
        buttonPressed.append(buttonPressed[0])
        print("Press",buttonPressed[0])
    elif data[0] == '2':
        positionPressed.append(data[1:5].index(buttonPressed[1])+1)
        buttonPressed.append(buttonPressed[1])
        print("Press",buttonPressed[1])
    elif data[0] == '3':
        positionPressed.append(data[1:5].index(buttonPressed[3])+1)
        buttonPressed.append(buttonPressed[3])
        print("Press",buttonPressed[3])
    else:
        positionPressed.append(data[1:5].index(buttonPressed[2])+1)
        buttonPressed.append(buttonPressed[2])
        print("Press",buttonPressed[2])
###END MEMORY###
###SEQUENCES###
occurences={"r":["c","b","a","ac","b","ac","abc","ab","b"],
            "b":["b","ac","b","a","b","bc","c","ac","a"],
            "k":["abc","ac","b","ac","b","bc","ab","c","c"]}
def cut2(n):
    if n:
        return ("Cut")
    else:
        return ("Don't cut")
def sequenceModule():
    ro=0
    bo=0
    ko=0
    while 1:
        data=input("x to escape, [color][connection]").strip().replace(" ", "").lower()
        if data == 'x':
            return
        if data[0] == 'r':
            print(cut2(data[-1] in occurences["r"][ro]))
            ro+=1
        elif data[0] == 'b':
            print(cut2(data[-1] in occurences['b'][bo]))
            bo+=1
        else:
            print(cut2(data[-1] in occurences['k'][ko]))
            ko+=1
###END SEQUENCES
###SIMON###
simonLookUp={True: {0:{'r':'b','b':'r','g':'y','y':'g'},1:{'r':'y','b':'g','g':'b','y':'r'},2:{'r':'g','b':'r','g':'y','y':'b'}},
             False:{0:{'r':'b','b':'y','g':'g','y':'r'},1:{'r':'r','b':'b','g':'y','y':'g'},2:{'r':'y','b':'g','g':'b','y':'r'}}
             }
def simonModule():
    s=0
    current=[]
    while 1:
        i=input("Input 0,1,2 to set strikes at any time, rgby for newest color, x to exit").strip().replace(" ", "").lower()
        if 'x' in i:
            return
        if '0' in i:
            s = 0
        elif '1' in i:
            s = 1
        elif '2' in i:
            s = 2
        if 'r' in i:
            current.append('r')
            simonHelp(current,s)
        elif 'g' in i:
            current.append('g')
            simonHelp(current,s)
        elif 'b' in i:
            current.append('b')
            simonHelp(current,s)
        elif 'y' in i:
            current.append('y')
            simonHelp(current,s)
def simonHelp(c,s):
    st=""
    for i in c:
        st+=simonLookUp[hasVowel()][s][i]+" "
    print(st)
    return
    
###END SIMON###
###COMPLICATED###
complicatedLookUp=['c','s','s','s','c','c','d','p','d','b','p','s','b','b','p','d']
def complicatedModule():
    while 1:
        i=input("x=exit, r=red, b=blue, l=LED on, s=star").strip().replace(" ", "").lower()
        if 'x' in i:
            return
        x=0
        if 'r' in i:
            x+=1
        if 'b' in i:
            x+=2
        if 's' in i:
            x+=4
        if 'l' in i:
            x+=8
        complicatedHelper(complicatedLookUp[x])
def complicatedHelper(val):
    if val == 'c':
        print("Cut")
    elif val == 's' and not lastDigitOdd():
        print("Cut")
    elif val == 'p' and hasParallel():
        print("Cut")
    elif val == 'b' and num_bat >1:
        print("Cut")
    else:
        print("Don't cut")
###END COMPLICATED
###MORSE###
morse=['shell','halls','slick','trick','boxes','leaks','strobe','bistro','flick','bombs','break','brick','steak','sting', 'vector', 'beats']

def morseModule():
    return
###END MORSE###

###MAZE###
import maze
def mazeModule():
    midf = maze.build_m1_identifier()
    kill = False
    pos1, pos2 = None, None
    found = midf.getMaze(pos1, pos2)
    while (not kill) and found == None:
        print("Enter 'x' to go back.")
        print("for testing: (4, 0), (1, 2)")
        maze.Maze().show(rulers=True)
        r1 = input("Enter row of first indicator point: ").strip().replace(" ", "")
        c1 = input("Enter column of first indicator point: ").strip().replace(" ", "")
        r2 = input("Enter row of second indicator point: ").strip().replace(" ", "")
        c2 = input("Enter column of second indicator point: ").strip().replace(" ", "")
        if "x" in (r1, c1, r2, c2):
            return
        try:
            r1, c1, r2, c2 = int(r1), int(c1), int(r2), int(c2)
            pos1 = (r1,c1)
            pos2 = (r2,c2)
            pass
        except Exception:
            print("Could not parse indicator point positions.")
            pass

        found = midf.getMaze(pos1, pos2)
        if not found:
            print("Could not find maze with those indicators, try again or exit with 'x'.")

    found.show()

    startR = input("Enter row of start: ").strip().replace(" ", "")
    startC = input("Enter column of start: ").strip().replace(" ", "")
    endR = input("Enter row of end: ").strip().replace(" ", "")
    endC = input("Enter column of end: ").strip().replace(" ", "")
    if "x" in (startR, startC, endR, endC):
        return
    try:
        startR, startC, endR, endC = int(startR), int(startC), int(endR), int(endC)
        pos1 = (startR, startC)
        pos2 = (endR, endC)
        print(maze.getSolutionInstructions(found, (startR,startC), (endR,endC) ))
        pass
    except Exception:
        print("Error with start/end positions.")
        pass
        return
###END MAZE###

while 1:
    which=input("Modules: (w)ire, (b)utton, s(i)mon, (f)irst, (m)emory, (c)omplicated, (s)equence, (p)assword, ma(z)e. > ").strip().replace(" ", "").lower()
    if "w" in which:
        wireModule()
    elif 'b' in which:
        buttonModule()
    elif 'i' in which:
        simonModule()
    elif 'f' in which:
        firstModule()
    elif 'm' in which:
        memoryModule()
    elif 'c' in which:
        complicatedModule()
    elif 's' in which:
        sequenceModule()
    elif 'p' in which:
        passModule()
    elif 'z' in which:
        mazeModule()
    else:
        print("unrecognized command")

