#written using python 3.13





def collectData(machineCode):
    tmInfo = {}
    TapesAlphas = []
    transitionRules = {}
    ruleNum = 1
    rulesLog = []
    actualLineCount = -1
    for i, line in enumerate(machineCode.splitlines()):
        if not line:
            continue

        actualLineCount += 1
        line = [item.strip() for item in line.split(",")]
        if actualLineCount == 0:
            #first line info
            tmInfo["name"] = line[0]
            tmInfo["tapesCount"] = int(line[1])
            tmTapes = tmInfo["tapesCount"] #for easy access in this function
            tmInfo["maxTapeSize"] = int(line[2])
            tmInfo["maxSteps"] = int(line[3])
        elif actualLineCount == 1:
            tmInfo["tmAlphabet"] = set(line) #the input on tape 1 also has a blank on the end in machine 1 and no blank on machine 2 very annoying not keeping format so look below for my weird checking
        elif actualLineCount == 2:
            tmInfo["states"] = set(line)
        elif actualLineCount == 3:
            tmInfo["startState"] = line[0]
        elif actualLineCount == 4:
            tmInfo["acceptState"] = line[0]
            tmInfo["rejectState"] = line[1]
        elif (actualLineCount < 5 + tmTapes): #triggers for lines defining the tape languages
            #tape alphabets stored
            line = set(line) #i need to do this looking at the input of example machine like tm2 ________ for tape 2
            line.add('_')
            TapesAlphas.append(line)
        else:
            #transitions stored
            rulesLog.append(f'Rule {ruleNum}:,{",".join(line)}')

            if line[0] not in tmInfo["states"]:
                return None
            if line[0] not in transitionRules:
                transitionRules[line[0]] = {}

            inputs = [] #need to go and make this updated format work in the loop of finding correct rule to travel
            for j in range(tmTapes):
                inputs.append(line[j+1])
            inputs = tuple(inputs)
            outputs = [line[tmTapes+1]] #collect next state and write and direction for head for each tape
            if line[tmTapes+1] not in tmInfo["states"]:
                return None
            for j in range(tmTapes + 2, len(line)):
                outputs.append(line[j])
            outputs = tuple(outputs)
            transitionRules[line[0]][inputs] = (outputs, ruleNum)
            ruleNum+= 1
    tmInfo["alphabets"] = TapesAlphas
    tmInfo["rules"] = transitionRules
    tmInfo["rulesLog"] = rulesLog
    return tmInfo

def simulate(machineCode, problemsCode): #one problem with # of tapes lines of input
    execution = []
    finalResult = ""
    tmInfo = collectData(machineCode)
    if not tmInfo:
        return {"error": "The machine had an error with rules not matching an existing state"}
    tmName = tmInfo["name"]
    tmTapes = tmInfo["tapesCount"]
    tmMaxTapeSize = tmInfo["maxTapeSize"]
    tmMaxSteps = tmInfo["maxSteps"]
    tmAlphabet = tmInfo["tmAlphabet"]
    tmStates = tmInfo["states"]
    tmStartState = tmInfo["startState"]
    tmAcceptState = tmInfo["acceptState"]
    tmRejectState = tmInfo["rejectState"]
    TapesAlphas = tmInfo["alphabets"]
    transitionRules = tmInfo["rules"]
    rulesLog = tmInfo["rulesLog"]



    TapeStarts = []
    temp = []
    error = False
    if len(problemsCode) != tmTapes: #problems code is a list of strings
        return {"error": f"Expected {tmInfo['tapesCount']} tapes, but got {len(problemsCode)}"}

    for j in range(tmTapes):
        TapeStarts.append(problemsCode[j]) #k-tuple storing each starting tape as strings in a array


    for j, tape in enumerate(TapeStarts): #go through this 1 problem is a array of strings
        print(f'Tape {j+1}: {tape}')
        if len(tape) > tmMaxTapeSize:
            return { "error": f"The input in tape {j} has too large of a size."}
        if j== 0:
            if tape[len(tape) - 1] not in tmAlphabet and tape[len(tape) - 1] != '_': #honestly confusing instruction but tm 1 has a _ at end, while tm2 doesn't so im assuming _ can decide to not or do show up only at end of input because reqs _ say not in input alpha
                return { "error": "Input Error on tape 1"}
            for k in range(len(tape)-1): #because test files have a _ at the end
                if tape[k] not in tmAlphabet:
                    return { "error": "Input Error on tape 1"}
            if error:
                break
        for k in range(len(tape)): #honestly the instructions about alphas are not good.
            if tape[k] not in TapesAlphas[j]:
                return { "error": f"Input Error on tape {j + 1}"}
                #error = True
                #break


        #now go and make each tape easier to use by making list and adding the extra _ at right
        TapeStarts[j] = (list(tape) + ['_'] * (tmMaxTapeSize - len(tape)))


    currSteps = 0

    currHead = [0] * tmTapes
    execution.append({
            "step": 0,
            "state": tmStartState,
            "heads": [0] * tmTapes,
            "tapes": ["".join(t) for t in TapeStarts],
            "ruleApplied": "Initial State"
        })

    currState = tmStartState
    if currState == tmAcceptState: #just for a trivial tm that has start accept or reject
        finalResult = "accept"
        return {
            "machineName": tmName,
            "simulation": {
                "status": finalResult,
                "finalStep": currSteps,
                "trace": execution, # The frontend can loop through this
                "finalTapes": ["".join(t) for t in TapeStarts]
            },
            "rulesReference": rulesLog #For showing the rulebook in the UI
        }

    elif currState == tmRejectState:
        finalResult = "reject"
        return {
            "machineName": tmName,
            "simulation": {
                "status": finalResult,
                "finalStep": currSteps,
                "trace": execution, # The frontend can loop through this
                "finalTapes": ["".join(t) for t in TapeStarts]
            },
            "rulesReference": rulesLog #For showing the rulebook in the UI
        }


    #TapeStarts acts as the array of tapes we use in this problem
    #now time to do the while loop to go through the simulation of this problem
    while currSteps < tmMaxSteps:
        currSteps += 1
        #currReading = [currState]
        currReading = []
        for i in range(tmTapes): #check if each head value is valid for that tape
            if TapeStarts[i][currHead[i]] not in TapesAlphas[i] and TapeStarts[i][currHead[i]] != '_':
                error = True
                break
            currReading.append(TapeStarts[i][currHead[i]])
        if error:
            return { "error": f"Alphabet Error on tape {i+1}"}
        currOutput = []


        currReading = tuple(currReading)
        if currState in transitionRules and currReading in transitionRules[currState]:
            currOutput = [currState, currReading, transitionRules[currState][currReading]]

        if not currOutput:#for wildcard cases
            for key, value in transitionRules[currState].items():
                for j in range(tmTapes): #check all tapes if the head val matchs the current rule or wildcard
                    if key[j] != currReading[j] and key[j] != '*':
                        break
                else:
                    currOutput = [currState, key, value] #found the correct rule
                    break

        if not currOutput: #if no rule found reject
            finalResult = "reject"
            break

        ruleID = currOutput[2][1]
        #found the correct transiton now simulate the things to do now
        currOutput = currOutput[2][0]
        currState = currOutput[0] #set current state
        for i in range(tmTapes): #for each tape write and move
            if currOutput[i+1] != '*': #write on tape if it didnt say dont write
                TapeStarts[i][currHead[i]] = currOutput[i+1]
            if currOutput[i + 1+ tmTapes] == 'R':
                currHead[i] += 1
            elif currOutput[i +1 + tmTapes] == 'L':
                currHead[i] -= 1
            if currHead[i] < 0: #if negative head set it to 0 and keep running
                currHead[i] = 0
            if currHead[i] >= tmMaxTapeSize: #too far out of tape if you wanted to just error if negative if currHead[i] < 0 or currHead[i] >= tmMaxTapeSize:
                return {"error": f"Tape Length Error on tape {i+1}"}
            

        execution.append({
                "step": currSteps,
                "state": currState,
                "heads": list(currHead),
                "tapes": ["".join(t) for t in TapeStarts],
                "ruleId": ruleID
        })

        if currState == tmAcceptState:
            finalResult = "accept"
            break
        elif currState == tmRejectState:
            finalResult = "reject"
            break



    if currSteps >=tmMaxSteps:
        return { "error": "too many steps for calculation"}

    return {
        "machineName": tmName,
        "simulation": {
            "status": finalResult,
            "finalStep": currSteps,
            "trace": execution, # The frontend can loop through this
            "finalTapes": ["".join(t) for t in TapeStarts]
        },
        "rulesReference": rulesLog #For showing the rulebook in the UI
    }









'''

def simulatemultiple(machineCode, problemsCode):
    history = []

    tmInfo = collectData(machineCode, history)
    if not tmInfo:
        return {"status": "The machine had an error with rules not matching an existing state"}
    tmName = tmInfo["name"]
    tmTapes = tmInfo["tapesCount"]
    tmMaxTapeSize = tmInfo["maxTapeSize"]
    tmMaxSteps = tmInfo["maxSteps"]
    tmAlphabet = tmInfo["tmAlphabet"]
    tmStates = tmInfo["states"]
    tmStartState = tmInfo["startState"]
    tmAcceptState = tmInfo["acceptState"]
    tmRejectState = tmInfo["rejectState"]
    TapesAlphas = tmInfo["alphabets"]
    transitionRules = tmInfo["rules"]

    inputLines = list(problemsCode.strip())

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
            printEndingTape(tmTapes, TapeStarts, history, "accept")
            continue
        elif currState == tmRejectState:
            print("Reject")
            printEndingTape(tmTapes, TapeStarts, history, "accept")
            continue

        currSteps = 0
        #TapeStarts acts as the array of tapes we use in this problem
        #now time to do the while loop to go through the simulation of this problem
        while currSteps < tmMaxSteps:
            currSteps += 1
            #currReading = [currState]
            currReading = []
            for i in range(tmTapes): #check if each head value is valid for that tape
                if TapeStarts[i][currHead[i]] not in TapesAlphas[i] and TapeStarts[i][currHead[i]] != '_':
                    error = True
                    break
                currReading.append(TapeStarts[i][currHead[i]])
            if error:
                printEndingTape(tmTapes, TapeStarts, history, f"Alphabet Error on tape {i+1}")
                break
            currOutput = []


            currReading = tuple(currReading)
            if currState in transitionRules and currReading in transitionRules[currState]:
                currOutput = [currState, currReading, transitionRules[currState][currReading]]

            if not currOutput:#for wildcard cases
                for key, value in transitionRules[currState].items():
                    for j in range(tmTapes): #check all tapes if the head val matchs the current rule or wildcard
                        if key[j] != currReading[j] and key[j] != '*':
                            break
                    else:
                        currOutput = [currState, key,value] #found the correct rule
                        break

            currHistory = {
                "step": currSteps,
                "state": currState,
                "reading": currReading,
                "ruleId": currOutput[2][1], #rule number 
                "heads": list(currHead),     #must make a copy of the list
                "tapes": ["".join(t) for t in TapeStarts]
            }
            history.append(currHistory)
            #found the correct transiton now simulate the things to do now
            currOutput = currOutput[2][0]
            currState = currOutput[0] #set current state
            if currState == tmAcceptState:
                printEndingTape(tmTapes, TapeStarts, history, "accept")
                break
            elif currState == tmRejectState:
                printEndingTape(tmTapes, TapeStarts, history, "reject")
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
                printEndingTape(tmTapes, TapeStarts, history, f"Tape Length Error on tape {i+1}")
                break

        if currSteps >=tmMaxSteps:
            printEndingTape(tmTapes, TapeStarts, history, "Error with too many steps for calculation")

    return history



'''