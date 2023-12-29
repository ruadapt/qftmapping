import copy

class gateType:
    def __init__(self, type, a1:tuple[int, int], a2:tuple[int, int]):
        self.type = type
        self.a1 = a1
        self.a2 = a2

def makepath(len:int, offpaths:set[int]):
    if any(map(lambda n:n>=len, offpaths)):
        raise Exception("Invalid path")
    
    out:list[list[int]] = [[], []]
    c = 0
    for i in range(len):
        out[0].append(c)
        c += 1
        if i in offpaths:
            out[1].append(c)
            c += 1
        else:
            out[1].append(None)
    #print(out)
    return out

def makeChildTracker(len:int):
    return [set() for _ in range(len)]

def addToTracker(tracker:list[set], i1:int, i2:int):
    n1 = min(i1, i2)
    n2 = max(i1, i2)
    if n2 in tracker[n1]:
        return "redundant"
    for i in range(0, n1):
        if n1 not in tracker[i]:
            print("Invalid n1: missing {} to {}".format(i, n1))
            return "illegal"
    tracker[n1].add(n2)
    for i in range(0, n2):
        if n2 not in tracker[i]:
            return "added"
    return "completed"

def procedure(glist:list[gateType], path:list[list[int, None]], nodeCount:int):
    tracker = makeChildTracker(nodeCount)
    indexRef = copy.deepcopy(path)
    confirmList = {0}
    
    marks = {0}
    while len(marks) > 0:
        marks:set = set()
        for i in range(0, len(path[0])):
            if path[1][i] == None:
                continue
            if path[0][i] in confirmList and path[1][i] not in confirmList:
                result = addToTracker(tracker, path[0][i], path[1][i])
                if result == 'illegal':
                    raise Exception(f"tracker error: {result} ({path[0][i]}->{path[1][i]})")
                if result == 'redundant':
                    continue
                if result == 'completed':
                    confirmList.add(path[1][i])
                glist.append(gateType('cr', (path[0][i], indexRef[0][i]), (path[1][i], indexRef[1][i])))
                glist.append(gateType('swap', (path[0][i], indexRef[0][i]), (path[1][i], indexRef[1][i])))
                temp = path[0][i]
                path[0][i] = path[1][i]
                path[1][i] = temp
            elif path[1][i] in confirmList and path[1][i] not in tracker[path[0][i]]:
                result = addToTracker(tracker, path[1][i], path[0][i])
                if result == 'illegal':
                    raise Exception(f"tracker error: {result} ({path[1][i]}->{path[0][i]})")
                if result == 'redundant':
                    continue
                if result == 'completed':
                    confirmList.add(path[0][i])
                glist.append(gateType('cr', (path[1][i], indexRef[1][i]), (path[0][i], indexRef[0][i])))
            else:
                continue
            marks.add(i)
        for i in range(1, len(path[0])):
            h = i-1
            if h in marks or i in marks:
                continue
            if path[0][h] in confirmList and path[0][i] not in confirmList:
                result = addToTracker(tracker, path[0][h], path[0][i])
                if result == 'redundant' or result == 'illegal':
                    raise Exception(f"tracker error: {result} ({path[0][h]}->{path[0][i]})")
                if result == 'completed':
                    confirmList.add(path[0][i])
                glist.append(gateType('cr', (path[0][h], indexRef[0][h]), (path[0][i], indexRef[0][i])))
                glist.append(gateType('swap', (path[0][h], indexRef[0][h]), (path[0][i], indexRef[0][i])))
                temp = path[0][h]
                path[0][h] = path[0][i]
                path[0][i] = temp
                marks.add(h)
                marks.add(i)
    #print(path)

# addrType: 0 for logical address, 1 for physical address
def displayGraph(gateList:list[gateType], nodeCount:int, addrType:int, printData:bool):

    stats = dict()
    stats['gateCount'] = 0
    stats['gateDepth'] = 0
    stats['swaps'] = 0

    #move and gate cancel
    organizedGates:list[list[gateType]] = [[] for i in range(nodeCount)]
    for gate in gateList:
        organizedGates[gate.a1[addrType]].append(gate)
        organizedGates[gate.a2[addrType]].append(gate)

    markedList = [0] * nodeCount
    while True:
        #print(list(map(lambda l:len(l), organizedGates)))
        if all(list(map(lambda l:len(l)==0, organizedGates))):
            break

        stats['gateDepth'] += 1

        markedList = [i-1 if i > 0 else i for i in markedList]
        
        if printData:
            outStr = ["."] * nodeCount
            addOn = ""
        
        for i in range(nodeCount):
            if len(organizedGates[i])==0:
                continue
            if markedList[i] > 0:
                continue
            gate = organizedGates[i][0]
            
            if markedList[gate.a1[addrType]] or organizedGates[gate.a1[addrType]][0] != gate:
                continue
            if markedList[gate.a2[addrType]] or organizedGates[gate.a2[addrType]][0] != gate:
                continue
            stats['gateCount'] += 1
            markedList[gate.a1[addrType]] = 1
            organizedGates[gate.a1[addrType]].pop(0)
            markedList[gate.a2[addrType]] = 1
            organizedGates[gate.a2[addrType]].pop(0)
            if gate.type == 'swap':
                stats['swaps'] += 1

            if printData:
                if gate.type == 'swap':
                    addOn += " SW({0},{1})".format(gate.a1[addrType], gate.a2[addrType])
                    left = min(gate.a1[addrType], gate.a2[addrType])
                    right = max(gate.a1[addrType], gate.a2[addrType])
                    outStr[left] = ">"
                    outStr[right] = "<"
                elif gate.type == 'cr':
                    addOn += " CR({0},{1})".format(gate.a1[addrType], gate.a2[addrType])
                    outStr[gate.a1[addrType]] = "c"
                    outStr[gate.a2[addrType]] = "O"    
        
        if printData:
            trueOutStr = ""
            for c in outStr:
                trueOutStr += c + " "
            print(trueOutStr + addOn)   
    return stats

def main():
    glist:list[gateType] = []

    l = 36              #main path  
    o = {3, 7, 11, 15}  #off path
    #o = {2, 4, 6, 8, 10, 12, 14, 16, 18}
    #o = {10, 20}
    #o = {}

    procedure(glist, makepath(l, o), l+len(o))

    stats = displayGraph(glist, l+len(o), 1, True)

    
    print("gate count: {}".format(len(glist)))
    print("total swaps: {}".format(stats['swaps']))
    print("total cycles: {}".format(stats['gateDepth']))

    tracker = makeChildTracker(l+len(o))
    completion = []

    for g in glist:
        #print("{} {} {}".format(g.type, g.n1, g.n2))
        if g.type == "cr":
            status = addToTracker(tracker, g.a1[0], g.a2[0])
            if status in ('redundant', 'illegal'):
                print(tracker)
                raise Exception(status)
            elif status == 'completed':
                completion.append(g.a2[0])
    if len(completion) != l+len(o)-1:
        raise Exception("incompletion")
    #print(tracker)

def iterTest():
    l = 20
    
    for i in range(l):
        print(f'\ntest: {i}')
        glist:list[gateType] = []

        o = {10, i}

        procedure(glist, makepath(l, o), l+len(o))

        stats = displayGraph(glist, l+len(o), 1, False)
        print("gate count: {}".format(len(glist)))
        print("total swaps: {}".format(stats['swaps']))
        print("total cycles: {}".format(stats['gateDepth']))

if __name__ == '__main__':
    main()





        
