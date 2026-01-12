import csv #output does not work properly in csv across colomns when double clicking after > .csv file  
#instead open blank excel > data > get data > from file > from txt/csv. That works idk why
#if you don't care about the csv req in the rubric this doesn't matter it shows up in console and .txt perfectly
import sys

#written using python 3.13
#execute via console/terminal with command python tm-24414164.py tm1.txt tm1-tape.txt


def printEndingTape(tmTapes, TapeStarts):
    for i in range(tmTapes):
        print(f'Tape {i+1}: {"".join(TapeStarts[i])}')

if len(sys.argv) != 3:
    print("Need 2 arguments of a tm file and tm input. Right now you did not specify those")
    sys.exit(1)
tmFile = sys.argv[1] #a string
inputFile = sys.argv[2] #a string

print("Starting my Project Turing simulator using file", tmFile)
TapesAlphas = []
transitionRules = []

ruleNum = 1
with open(tmFile, mode='r', newline='') as file: #open machine file read info and save
    reader = csv.reader(file)
    for i, tmInfo in enumerate(reader):
        if i == 0:
            #first line info
            tmName = tmInfo[0]
            tmTapes = int(tmInfo[1])
            tmMaxTapeSize = int(tmInfo[2])
            tmMaxSteps = int(tmInfo[3])
        elif i == 1:
            tmAlphabet = set(tmInfo) #the input on tape 1 also has a blank on the end in machine 1 and no blank on machine 2 very annoying not keeping format so look below for my weird checking
        elif i == 2:
            tmStates = tmInfo
        elif i == 3:
            tmStartState = tmInfo[0]
        elif i == 4:
            tmAcceptState = tmInfo[0]
            tmRejectState = tmInfo[1]
        elif (i < 5 + tmTapes): #triggers for lines defining the tape languages
            #tape alphabets stored
            tmInfo = set(tmInfo) #i need to do this looking at the input of example machine like tm2 ________ for tape 2 
            tmInfo.add('_') #despite the instructions saying automatically added do not add, the files dont have that so im adding it here
            TapesAlphas.append(tmInfo)
        else:
            #transitions stored
            print(f'Rule {ruleNum}:,{",".join(tmInfo)}')
            inputs = [tmInfo[0]] #input list has curr state and the needed items at tape heads.
            for j in range(tmTapes):
                inputs.append(tmInfo[j+1])
            outputs = [tmInfo[tmTapes+1]] #collect next state and write and direction for head for each tape
            for j in range(tmTapes + 2, len(tmInfo)):
                outputs.append(tmInfo[j])
            transitionRules.append([inputs,  outputs, ruleNum])
            ruleNum+= 1


print("Using input file", inputFile) #now using the problem file
with open(inputFile, "r") as file:
    inputLines = []
    for i in file:
        inputLines.append(i.strip()) #read the entire file

for eachproblem in range(0, len(inputLines), tmTapes): #outer loop for going through all problems
    print("Trying Problem", eachproblem//tmTapes +1)
    TapeStarts = []
    temp = []
    error = False
    for j in range(eachproblem, eachproblem + tmTapes):
        TapeStarts.append(inputLines[j]) #k-tuple storing each starting tape as strings in a array
    for j, tape in enumerate(TapeStarts): #go through this 1 problem is a array of strings
        print(f'Tape {j+1}: {tape}')
        if len(tape) > tmMaxTapeSize:
            print(f"The input in tape {j} has too large of a size.")
            error = True
            break
        if j== 0:
            if tape[len(tape) - 1] not in tmAlphabet and tape[len(tape) - 1] != '_': #honestly confusing instruction but tm 1 has a _ at end, while tm2 doesn't so im assuming _ can decide to not or do show up only at end of input because reqs _ say not in input alpha
                print("Input Error on tape 1")
                error = True
                break
            for k in range(len(tape)-1): #because test files have a _ at the end
                if tape[k] not in tmAlphabet:
                    print("Input Error on tape 1")
                    error = True
                    break
            if error:
                break
        for k in range(len(tape)): #honestly the instructions about alphas are not good.
            if tape[k] not in TapesAlphas[j]:
                print(f"Input Error on tape {j + 1}")
                error = True
                break
        if error:
            break
        #now go and make each tape easier to use by making list and adding the extra _ at right
        TapeStarts[j] = (list(tape) + ['_'] * (tmMaxTapeSize - len(tape)))
    if error:
        continue #to next problem don't show the tape strings because this problem had errors on tape input not good

    currHead = [0] * tmTapes
    currState = tmStartState
    if currState == tmAcceptState: #just for a trivial tm that has start accept or reject
        print("Accept")
        printEndingTape(tmTapes, TapeStarts)
        continue
    elif currState == tmRejectState:
        print("Reject")
        printEndingTape(tmTapes, TapeStarts)
        continue

    currSteps = 0
    #TapeStarts acts as the array of tapes we use in this problem
    #now time to do the while loop to go through the simulation of this problem
    while currSteps < tmMaxSteps:
        currSteps += 1
        currReading = [currState]
        for i in range(tmTapes): #check if each head value is valid for that tape
            if TapeStarts[i][currHead[i]] not in TapesAlphas[i] and TapeStarts[i][currHead[i]] != '_':
                error = True
                break
            currReading.append(TapeStarts[i][currHead[i]])
        if error:
            print(f"Alphabet Error on tape {i+1}")
            printEndingTape(tmTapes, TapeStarts)
            break
        currOutput = []
        for i in transitionRules: #look through all rules for an exact match
            if currReading[0] != i[0][0]: #skip if rule does not apply to correct state
                continue
            for j in range(tmTapes): #check all tapes if the head val matchs the current rule
                if i[0][j+1] != currReading[j+1]:
                    break
            else:
                currOutput = i #found the correct rule
                break
        if not currOutput: #now look accepting read wildcard rules
            for i in transitionRules: #look through all rules
                if currReading[0] != i[0][0]: #skip if rule does not apply to correct state
                    continue
                for j in range(tmTapes): #check all tapes if the head val matchs the current rule or wildcard
                    if i[0][j+1] != currReading[j+1] and i[0][j+1] != '*':
                        break
                else:
                    currOutput = i #found the correct rule
                    break

        if not currOutput: #if no rule found reject
            print("Reject, No valid transition step found")
            error = True
            printEndingTape(tmTapes, TapeStarts)
            break
        #print(currSteps, currOutput[2], *currHead, *currOutput[0], *currOutput[1], sep = ',')
        print(f'{currSteps},{currOutput[2]},{','.join(map(str, currHead))},{','.join(currOutput[0])},{','.join(currOutput[1])}')
        #found the correct transiton now simulate the things to do now
        currOutput = currOutput[1]
        currState = currOutput[0] #set current state
        if currState == tmAcceptState:
            print("Accept")
            printEndingTape(tmTapes, TapeStarts)
            break
        elif currState == tmRejectState:
            print("Reject")
            printEndingTape(tmTapes, TapeStarts)
            break
        for i in range(tmTapes): #for each tape write and move
            if currOutput[i+1] != '*': #write on tape if it didnt say dont write
                TapeStarts[i][currHead[i]] = currOutput[i+1]
            if currOutput[i + 1+ tmTapes] == 'R':
                currHead[i] += 1
            elif currOutput[i +1 + tmTapes] == 'L':
                currHead[i] -= 1
            if currHead[i] < 0: #following textbook def, if negative head set it to 0 and keep running
                currHead[i] = 0
            if currHead[i] >= tmMaxTapeSize: #too far out of tape if you wanted to just error if negative if currHead[i] < 0 or currHead[i] >= tmMaxTapeSize:
                #print("Reading error past acceptable tape length on tape", i+1) #the rubric doesnt want be to specify the error type because of csv requirement
                error = True
                break
        if error:
            print(f"Tape Length Error on tape {i+1}") #
            printEndingTape(tmTapes, TapeStarts)
            break

    if currSteps >=tmMaxSteps:
        print("Steps Amount Error")
        printEndingTape(tmTapes, TapeStarts)



