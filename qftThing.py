
class gateType:
    def __init__(self, type, n1, n2):
        self.type = type
        self.n1 = n1
        self.n2 = n2

def makegrid(w:int, h:int):
    out:list[list[int]] = []
    c = 0
    for _ in range(h):
        row = []
        for _ in range(w):
            row.append(c)
            c += 1
        out.append(row)
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

def listSwap(inList:list, r1:int, r2:int):
    temp = inList[r1]
    inList[r1] = inList[r2]
    inList[r2] = temp
    return inList

def procedure1D(gatelist:list[gateType], inList:list[int], rowIndex:int = 0, isReverse = False):
    tracker = makeChildTracker(len(inList))
    listLen = len(inList)
    indexList:list[int] = [i for i in range(listLen)]
    if isReverse:
        indexList.reverse()

    #H gate?
    for i in [j for j in range(0, listLen-1)] + [j for j in range(listLen-3, -1, -1)]:
        for z in range(i, -1, -2):
            z1 = z
            z2 = z+1
            if isReverse:
                z1 = listLen - z - 1
                z2 = listLen - z2 - 1
            #print(z1, z2, inList[z1], inList[z2])
            status = addToTracker(tracker, indexList[z1], indexList[z2])
            #print(status)
            if status in ('added', 'completed'):
                gatelist.append(gateType('cr', inList[z1], inList[z2]))
                #H gate?
                pass
            gatelist.append(gateType('swap', inList[z1], inList[z2]))
            inList = listSwap(inList, z1, z2)
            indexList = listSwap(indexList, z1, z2)
            #print(inList)
    #print(tracker)
def procedureInter(gatelist:list[gateType], inList:list[list[int]], rowIndex1:int, rowIndex2:int):
    procedureInter2(gatelist, inList, rowIndex1, rowIndex2)

#NAIVE METHOD
def procedureInter1(gatelist:list[gateType], inList:list[list[int]], rowIndex1:int, rowIndex2:int):
    row1 = inList[rowIndex1]
    row2 = inList[rowIndex2]
    rowLen = len(inList[0])
    indexList1:list[int] = [i for i in range(rowLen)]
    localTracker = [set() for _ in range(rowLen)]

    offsets = [-1] + [j for j in range(0, rowLen-1)] + [j for j in range(rowLen-3, -1, -1)] + [-1]
    for i in range(1, len(offsets)):
        #print(row1, row2)

        for x in range(rowLen):
            if row2[x] not in localTracker[indexList1[x]]:
                localTracker[indexList1[x]].add(row2[x])
                gatelist.append(gateType('cr', row1[x], row2[x]))

        i2 = i-1
        for z in range(offsets[i], -1, -2):
            z1 = z
            z2 = z+1
            gatelist.append(gateType('swap', row1[z1], row1[z2]))
            row1 = listSwap(row1, z1, z2)
            indexList1 = listSwap(indexList1, z1, z2)
        for z in range(offsets[i2], -1, -2):
            z1 = z
            z2 = z+1
            gatelist.append(gateType('swap', row2[z1], row2[z2]))
            row2 = listSwap(row2, z1, z2)
        pass
    #print(row1, row2)
    #print(localTracker)


def procedureInter2(gatelist:list[gateType], inList:list[list[int]], rowIndex1:int, rowIndex2:int):
    row1 = inList[rowIndex1]
    row2 = inList[rowIndex2]
    rowLen = len(inList[0])
    indexList1:list[int] = [i for i in range(rowLen)]
    localTracker = [set() for _ in range(rowLen)]

    for i in range(0, rowLen):
        #print(row1, row2)

        for x in range(rowLen):
            if row2[x] not in localTracker[indexList1[x]]:
                localTracker[indexList1[x]].add(row2[x])
                gatelist.append(gateType('cr', row1[x], row2[x]))
        len1 = rowLen-2
        len2 = rowLen-2
        if i%2 == 1:
            len1 -= 1
        else:
            len2 -= 1
        for z in range(len1, -1, -2):
            z1 = z
            z2 = z+1
            gatelist.append(gateType('swap', row1[z1], row1[z2]))
            row1 = listSwap(row1, z1, z2)
            indexList1 = listSwap(indexList1, z1, z2)
        for z in range(len2, -1, -2):
            z1 = z
            z2 = z+1
            gatelist.append(gateType('swap', row2[z1], row2[z2]))
            row2 = listSwap(row2, z1, z2)
        pass
    #print(row1, row2)
    #print(localTracker)

def procedure2D(gatelist:list[gateType], inList:list[list[int]]):
    tracker = makeChildTracker(len(inList))
    listLen = len(inList)
    indexList:list[int] = [i for i in range(listLen)]

    listOrders = [False] * listLen

    procedure1D(gatelist, inList[0], 0)
    listOrders[0] = not listOrders[0]

    for i in [j for j in range(0, listLen-1)] + [j for j in range(listLen-3, -1, -1)]:
        for z in range(i, -1, -2):
            z1 = z
            z2 = z+1
            #print(z1, z2, inList[z1], inList[z2])
            status = addToTracker(tracker, indexList[z1], indexList[z2])
            #print(status)
            if status in ('added', 'completed'):
                #cr
                procedureInter(gatelist, inList, z1, z2)
                listOrders[z1] = not listOrders[z1]
                listOrders[z2] = not listOrders[z2]

                if status == 'completed':
                    procedure1D(gatelist, inList[z2], z2, isReverse=listOrders[z2])
                    listOrders[z2] = not listOrders[z2]

            for k in range(len(inList[0])):
                gatelist.append(gateType('swap', inList[z1][k], inList[z2][k]))
            inList = listSwap(inList, z1, z2)
            indexList = listSwap(indexList, z1, z2)
            listOrders = listSwap(listOrders, z1, z2)
            #print(inList)
    #print(tracker)

def displayGraph(gateList:list[gateType], nodeCount:int):

    stats = dict()
    stats['gateDepth'] = 0
    stats['swaps'] = 0

    #move and gate cancel
    organizedGates:list[list[gateType]] = [[] for i in range(nodeCount)]
    for gate in gateList:
        organizedGates[gate.n1].append(gate)
        organizedGates[gate.n2].append(gate)

    markedList = [0] * nodeCount
    while True:
        #print(list(map(lambda l:len(l), organizedGates)))
        if all(list(map(lambda l:len(l)==0, organizedGates))):
            break

        stats['gateDepth'] += 1

        markedList = [i-1 if i > 0 else i for i in markedList]
        
        #outStr = ["."] * nodeCount
        #addOn = ""
        
        for i in range(nodeCount):
            if len(organizedGates[i])==0:
                continue
            if markedList[i] > 0:
                continue
            gate = organizedGates[i][0]
            
            if markedList[gate.n1] or organizedGates[gate.n1][0] != gate:
                continue
            if markedList[gate.n2] or organizedGates[gate.n2][0] != gate:
                continue
            #stats['gateCount'] += 1
            markedList[gate.n1] = 1
            organizedGates[gate.n1].pop(0)
            markedList[gate.n2] = 1
            organizedGates[gate.n2].pop(0)
            if gate.type == 'swap':
                stats['swaps'] += 1

            #if gate.type == 'swap':
                #addOn += " SW({0},{1})".format(gate.n1, gate.n2)
                #left = min(gate.n1, gate.n2)
                #right = max(gate.n1, gate.n2)
                #outStr[left] = ">"
                #outStr[right] = "<"
            #elif gate.type == 'cr':
                #addOn += " CR({0},{1})".format(gate.n1, gate.n2)
                #outStr[gate.n1] = "c"
                #outStr[gate.n2] = "O"    
        
        #trueOutStr = ""
        #for c in outStr:
        #    trueOutStr += c + " "
        #print(trueOutStr + addOn)   
    return stats

def main():
    glist:list[gateType] = []

    w = 50
    h = 50

    procedure2D(glist, makegrid(w, h))

    stats = displayGraph(glist, w*h)

    tracker = makeChildTracker(w*h)
    completion = []

    print("gate count: {}".format(len(glist)))
    print("total swaps: {}".format(stats['swaps']))
    print("total cycles: {}".format(stats['gateDepth']))

    for g in glist:
        #print("{} {} {}".format(g.type, g.n1, g.n2))
        if g.type == "cr":
            status = addToTracker(tracker, g.n1, g.n2)
            if status in ('redundant', 'illegal'):
                print(tracker)
                raise Exception(status)
            elif status == 'completed':
                completion.append(g.n2)
    if len(completion) != w*h-1:
        raise Exception("incompletion")
    #print(tracker)

main()





        
