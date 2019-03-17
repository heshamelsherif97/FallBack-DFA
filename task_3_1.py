import argparse, re

class DfaState:
    def __init__(self, name):
        self.transitions = {}
        self.name = name
        self.regDef = ""
        self.action= ""
        self.isDead = False
        self.isEnd = False

class DFA:
    def __init__(self):
        self.states = []
        self.sortedStates = []
        self.alphabet = []
        self.start = ""
        self.endStates = []

    def filterLines(self, lines):
        newList = []
        for i in lines:
            newList.append(i.replace("\n", ""))
        return newList

    def setStart(self, start):
        for i in self.states:
            if i.name == start:
                self.start = i

    def sortStates(self, states):
        for i in states.split(", "):
            self.sortedStates.append(self.getStateByName(i))

    def parseInput(self, lines):
        lines = self.filterLines(lines)
        self.alphabet = lines[1].split(", ")
        end = lines[3].split(", ")
        transitions = lines[4]
        regDef = lines[5]
        actions = lines[6]
        self.addAllStates(transitions)
        self.setStart(lines[2])
        self.handleDead()
        self.handleEnd(end)
        self.handleReg(regDef)
        self.handleActions(actions)
        self.sortStates(lines[0])

    def handleDead(self):
        for i in self.states:
            if i.name == "DEAD":
                i.isDead = True

    def handleEnd(self, end):
        for i in self.states:
            if i.name in end:
                i.isEnd = True
                self.endStates.append(i)


    def addActions(self, actions):
        regDef = actions[0]
        action = actions[1]
        for i in self.states:
            if i.regDef == regDef:
                i.action = action

    def addReg(self, reg):
        state = reg[0]
        regDef = reg[1]
        for i in self.states:
            if i.name == state:
                i.regDef = regDef

    def handleActions(self, actions):
        splitted = re.findall(r'\(\"[^\"]+\"\, \"[^\"]+\"\)', actions)
        parseTransition = []
        for i in splitted:
            new = i.replace("(", "")
            new = new.replace(")", "")
            parseTransition.append(new)
        finalParse = []
        for i in parseTransition:
            finalParse = i.split(", ")
            self.addActions(finalParse)

    def handleReg(self, regDef):
        splitted = re.findall("\(\w+\, \"[^\"]+\"\)", regDef)
        parseTransition = []
        for i in splitted:
            new = i.replace("(", "")
            new = new.replace(")", "")
            parseTransition.append(new)
        finalParse = []
        for i in parseTransition:
            finalParse = i.split(", ")
            self.addReg(finalParse)

    def addAllStates(self, transitions):
        splitted = re.findall(r'\(\w+\, \w?\, \w+\)', transitions)
        parseTransition = []
        for i in splitted:
            new = i.replace("(", "")
            new = new.replace(")", "")
            parseTransition.append(new)
        finalParse = []
        for i in parseTransition:
            finalParse = i.split(", ")
            self.handleAddingStates(finalParse)

    def checkStateName(self, name):
        for i in self.states:
            if i.name == name:
                return False
        return True


    def getStateByName(self, name):
        for i in self.states:
            if i.name == name:
                return i
        
    def handleAddingStates(self, finalParse):
        s1 = finalParse[0]
        trans = finalParse[1]
        s2 = finalParse[2]
        if self.checkStateName(s1):
            s11 = DfaState(s1)
            self.states.append(s11)
        if self.checkStateName(s2):
            s12 = DfaState(s2)
            self.states.append(s12)
        self.getStateByName(s1).transitions[trans] = self.getStateByName(s2)


    def printResult(self, x):
        output_file = open("task_3_1_result.txt", "w+", encoding="utf-8")
        for i in x:
            output_file.write(i + "\n") 


    def printLexem(self, i, j, word, state):
        if j < i:
            j = len(word) - 1
        p = ""
        while i <= j:
            p += word[i]
            i += 1
        p += ", " + state.action
        return p

    def fallback(self, lines):
        inputIn = lines[0]
        i = 0
        check = True
        newList = []
        while i < len(inputIn):
            active = self.start
            fallStack = []
            fallStack.append(active)
            j = i
            while j < len(inputIn):
                active = active.transitions[inputIn[j]]
                fallStack.append(active)
                j += 1
            poped = ""
            while len(fallStack)!=0:
                poped = fallStack.pop()
                j -= 1
                if poped.isEnd:
                    break
                if len(fallStack) == 0:
                    check = False 
            newList.append(self.printLexem(i, j, inputIn, poped))
            if not check:
                break
            i = j + 1
        self.printResult(newList)

            
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--dfa-file', action="store", help="path of file to take as input to construct DFA", nargs="?", metavar="dfa_file")
    parser.add_argument('--input-file', action="store", help="path of file to take as input to test strings in on DFA", nargs="?", metavar="input_file")
    
    args = parser.parse_args()
    lines = []
    lines2 = []
    with open(args.dfa_file, "r") as f:
        for line in f:
            lines.append(line)
    with open(args.input_file, "r") as f:
        for line in f:
            lines2.append(line)
    x = DFA()
    x.parseInput(lines)
    x.fallback(lines2)
    print(args.dfa_file)
    print(args.input_file)


