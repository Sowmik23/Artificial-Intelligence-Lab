import math
import collections
import copy
import time
import queue


mp = collections.ChainMap()
indx = 0
isVisited = collections.ChainMap()
call = 0
Node = []

class node:
    def __init__(self,state,parent,action,g_cost,depth,h_cost,x,y,move,ck):
        self.state = state
        self.parent = parent
        self.action = action
        self.g_cost = g_cost
        self.depth = depth
        self.h_cost = h_cost
        self.x=x
        self.y=y
        self.move=move
        self.ck=ck

    def __lt__(self, other):
        # print("ok",  self.ck)
        if self.ck == 0:
            return self.g_cost<other.g_cost
        elif self.ck == 1:
            # if self.h_cost!=other.h_cost:
                return self.h_cost<other.h_cost
            # return self.depth<other.depth
        elif self.ck == 2:
            # if (self.h_cost+self.g_cost)!=(other.h_cost+other.g_cost):
                return (self.h_cost+self.g_cost)<(other.h_cost+other.g_cost)
            # return self.depth<other.depth


def initAcState(acState):
    cnt = 1
    row = len(acState)
    for i in range(0,row):
        for j in range(0,row):
            acState[i][j]=cnt
            cnt+=1
    acState[row-1][row-1]= 0



def prntState(state):
    row = len(state)
    for i in range(row):
        for j in range(row):
            print(state[i][j],end=" ")
        print("")
    print("")

def filePrint(file,state):
    row = len(state)
    for i in range(row):
        for j in range(row):
            file.write(str(state[i][j])+" ")
        file.write("\n")
    file.write("\n")

def getAction(x,y):
    lmt = row-1
    rslt = []
    if x<lmt:
        rslt+=["down"]
    if x>0:
        rslt+=["up"]
    if y<lmt:
        rslt+=["right"]
    if y>0:
        rslt+=["left"]

    return rslt

def movCheck(mov,x,y):
    if mov =="up":
        X=x-1
        Y=y
    elif mov == "down":
        X=x+1
        Y=y
    elif mov =="right":
        X=x
        Y=y+1
    elif mov =="left":
        X=x
        Y=y-1
    return X,Y

def listToString(tmp):
    strr =""
    for i in range(len(tmp)):
        for j in range(len(tmp)):
            strr+=str(tmp[i][j])
            strr+=' '
    return strr

def heuristic(tmpState,ck):
    row = len(tmpState)
    cnt = 0
    if ck == 1:
        for i in range(0, row):
            for j in range(0, row):
                if (tmpState[i][j]!=acState[i][j]) and tmpState[i][j]!=0:
                    cnt+=1

    elif ck == 2:
        mpp= collections.ChainMap()
        for i in range(0, row):
            for j in range(0, row):
                mpp[acState[i][j]]=[i,j]
        for i in range(0, row):
            for j in range(0, row):
                tmp = mpp[tmpState[i][j]]
                cnt+=(abs(i-tmp[0])+abs(j-tmp[1]))

    return cnt



def BFS(tmpNode):
    queuee = []
    queuee.append(tmpNode)
    isVisited[listToString(tmpNode.state)] = 1

    while len(queuee) !=0:
        nd = queuee.pop(0)
        x=nd.x
        y=nd.y
        global call
        call+=1
        if nd.state==acState:
            return nd
        for mov in nd.action:
            X,Y=movCheck(mov,x,y)
            nwstate = copy.deepcopy(nd.state)
            nwstate[x][y]=nd.state[X][Y]
            nwstate[X][Y] = nd.state[x][y]
            tmp=listToString(nwstate)
            nwNode = node(nwstate,mp[listToString(nd.state)],getAction(X,Y),nd.g_cost,nd.depth+1,nd.h_cost,X,Y,mov,0)
            if tmp not in mp:
                global indx
                mp[tmp]=indx
                indx+=1
                global Node
                Node+=[nwNode]
            if nwstate==acState:
                return nwNode

            if tmp not in isVisited:
                queuee.append(nwNode)
                isVisited[tmp] = 1

    return None

def UCS(tmpNode):
    q = queue.PriorityQueue()
    q.put(tmpNode)
    isVisited[listToString(tmpNode.state)] = 1

    while not q.empty():
        nd = q.get()
        x=nd.x
        y=nd.y
        global call
        call+=1
        isVisited[listToString(nd.state)] = 2
        if nd.state==acState:
            return nd
        for mov in nd.action:
            X,Y=movCheck(mov,x,y)
            nwstate = copy.deepcopy(nd.state)
            nwstate[x][y]=nd.state[X][Y]
            nwstate[X][Y] = nd.state[x][y]
            tmp=listToString(nwstate)
            nwNode = node(nwstate,mp[listToString(nd.state)],getAction(X,Y),nd.g_cost+1,nd.depth+1,nd.h_cost,X,Y,mov,0)
            if tmp not in mp:
                global indx
                mp[tmp]=indx
                indx+=1
                global Node
                Node+=[nwNode]

            if tmp not in isVisited:
                q.put(nwNode)
                isVisited[tmp] = 1
            elif isVisited[tmp]==1:
                q.put(nwNode)
    return None

def DLS(tmpNode,cutOffNode,limit):

    isVisited[listToString(tmpNode.state)] = 1

    nd = copy.deepcopy(tmpNode)
    x=nd.x
    y=nd.y
    global call
    call+=1
    if nd.state==acState:
        return nd
    elif limit==0:
        return cutOffNode
    isCutOff = False
    for mov in nd.action:

        X,Y=movCheck(mov,x,y)

        nwstate = copy.deepcopy(nd.state)
        nwstate[x][y]=nd.state[X][Y]
        nwstate[X][Y] = nd.state[x][y]
        tmp=listToString(nwstate)
        nwNode = node(nwstate,mp[listToString(nd.state)],getAction(X,Y),nd.g_cost,nd.depth+1,nd.h_cost,X,Y,mov,0)
        if nwstate==acState:
            return nwNode

        if tmp not in mp:
            global indx
            mp[tmp]=indx
            indx+=1
            global Node
            Node+=[nwNode]

            rslt = DLS(nwNode, cutOffNode, limit - 1)
            if rslt == cutOffNode:
                isCutOff = True
            elif rslt != None:
                return rslt
        else :
            chk=mp[tmp]
            chkNode = Node[chk]
            if chkNode.depth > nwNode.depth:
                Node[chk]=nwNode
                rslt = DLS(nwNode, cutOffNode, limit - 1)
                if rslt == cutOffNode:
                    isCutOff = True
                elif rslt != None:
                    return rslt

    if isCutOff == True:
        return cutOffNode
    else:
        return None

def GBFS(tmpNode,chk):

    q = queue.PriorityQueue()
    q.put(tmpNode)
    isVisited[listToString(tmpNode.state)] = 1

    while not q.empty():
        nd = q.get()
        x=nd.x
        y=nd.y
        global call
        call+=1
        isVisited[listToString(nd.state)] = 2
        if nd.state==acState:
            return nd
        for mov in nd.action:
            X,Y=movCheck(mov,x,y)
            nwstate = copy.deepcopy(nd.state)
            nwstate[x][y]=nd.state[X][Y]
            nwstate[X][Y] = nd.state[x][y]
            tmp=listToString(nwstate)
            cost = heuristic(nwstate,chk)
            nwNode = node(nwstate,mp[listToString(nd.state)],getAction(X,Y),nd.g_cost,nd.depth+1,cost,X,Y,mov,1)

            if tmp not in isVisited:
                global indx
                mp[tmp] = indx
                indx += 1
                global Node
                Node += [nwNode]

                q.put(nwNode)
                isVisited[tmp] = 1

            # if isVisited[tmp]==1:
            #     chk = mp[tmp]
            #     chkNode = Node[chk]
            #     if chkNode.depth > nwNode.depth:
            #         Node[chk] = nwNode
            #     q.put(nwNode)

    return None

def A_star(tmpNode,chk):
    q = queue.PriorityQueue()
    q.put(tmpNode)
    isVisited[listToString(tmpNode.state)] = 1

    while not q.empty():
        nd = q.get()
        x=nd.x
        y=nd.y
        global call
        call+=1
        isVisited[listToString(nd.state)] = 2
        if nd.state==acState:
            return nd
        for mov in nd.action:
            X,Y=movCheck(mov,x,y)
            nwstate = copy.deepcopy(nd.state)
            nwstate[x][y]=nd.state[X][Y]
            nwstate[X][Y] = nd.state[x][y]
            tmp=listToString(nwstate)
            cost = heuristic(nwstate,chk)
            nwNode = node(nwstate,mp[listToString(nd.state)],getAction(X,Y),nd.g_cost+1,nd.depth+1,cost,X,Y,mov,2)

            if tmp not in isVisited:
                global indx
                mp[tmp] = indx
                indx += 1
                global Node
                Node += [nwNode]

                q.put(nwNode)
                isVisited[tmp] = 1
            # if isVisited[tmp]==1:
            #     chk = mp[tmp]
            #     chkNode = Node[chk]
            #     if chkNode.depth > nwNode.depth:
            #         Node[chk] = nwNode
            #     q.put(nwNode)

    return None

def call_BFS(tmpState):
    file = open("output_BFS.txt", "w")
    file.write("Initial state :\n")
    filePrint(file, tmpState)

    mp.clear()
    global indx
    indx = 0
    tmp = listToString(tmpState.copy())
    mp[tmp] = indx
    indx += 1
    global Node
    Node = []
    global call
    call = 0
    tmpNode = node(state=tmpState, parent=-1, action=getAction(srtX, srtY), g_cost=0, depth=0, h_cost=0, x=srtX, y=srtY,
                   move="intit",ck=0)
    Node += [tmpNode]
    isVisited.clear()

    startTime = time.time()
    print("Running BFS........")
    nd = BFS(tmpNode)
    print("End of BFS.......")
    elapsedTime = time.time() - startTime

    if nd == None:
        print("Not found AC state.....")
        file.write("Not found AC state.....\n")
        file.write("Total call: " + str(call) + "\nTotal node Create: " + str(indx) + "\nElapsed Time : " + str(
            elapsedTime) + "\n")
    else:
        # print(nd.depth, call, indx)
        print("Found AC state")
        file.write("Depth is: " + str(nd.depth) + "\nTotal call: " + str(call) + "\nTotal node Create: " + str(
            indx) + "\nElapsed Time : " + str(elapsedTime) + "\n\n")
        answer = []
        tmpnd = copy.deepcopy(nd)
        while tmpnd.parent != -1:
            answer += [tmpnd]
            tmpnd = Node[tmpnd.parent]
        answer.reverse()
        for nn in answer:
            file.write("move :" + nn.move + "\n")
            filePrint(file, nn.state)
        file.close()

def call_UCS(tmpState):
    file = open("output_UCS.txt", "w")

    # prntState(tmpState)
    file.write("Initial state :\n")
    filePrint(file, tmpState)

    mp.clear()
    global indx
    indx = 0
    tmp = listToString(tmpState.copy())
    mp[tmp] = indx
    indx += 1
    global Node
    Node = []
    global call
    call = 0
    tmpNode = node(state=tmpState, parent=-1, action=getAction(srtX, srtY), g_cost=0, depth=0, h_cost=0, x=srtX, y=srtY,
                   move="intit",ck=0)
    Node += [tmpNode]
    isVisited.clear()

    startTime = time.time()
    print("UCS running......")
    nd = UCS(tmpNode)
    print("End of UCS...........")
    elapsedTime = time.time() - startTime
    if nd == None:
        print("Not found AC state.....")
        file.write("Not found AC state.....\n")
        file.write("Total call: " + str(call) + "\nTotal node Create: " + str(indx) + "\nElapsed Time : " + str(
            elapsedTime) + "\n")
    else:
        # print(nd.depth, call, indx)
        print("Found AC state")
        file.write("Cost is: " + str(nd.g_cost) + "\nTotal call: " + str(call) + "\nTotal node Create: " + str(
            indx) + "\nElapsed Time : " + str(elapsedTime) + "\n\n")
        answer = []
        tmpnd = copy.deepcopy(nd)

        while tmpnd.parent != -1:
            answer += [tmpnd]
            tmpnd = Node[tmpnd.parent]
        answer.reverse()
        for nn in answer:
            file.write("move :" + nn.move + "\n")
            filePrint(file, nn.state)
        file.close()

def call_DLS(tmpState,limit):
    file = open("output_DLS.txt", "w")

    # prntState(tmpState)
    file.write("Initial state :\n")
    filePrint(file, tmpState)

    mp.clear()
    global indx
    indx = 0
    tmp = listToString(tmpState.copy())
    mp[tmp] = indx
    indx += 1
    global Node
    Node = []
    global call
    call = 0
    tmpNode = node(state=tmpState, parent=-1, action=getAction(srtX, srtY), g_cost=0, depth=0, h_cost=0, x=srtX, y=srtY,
                   move="intit",ck=0)
    Node += [tmpNode]
    cutOffNode = node(state=tmpState, parent=-5, action=getAction(srtX, srtY), g_cost=-1, depth=-1, h_cost=-1, x=srtX, y=srtY,
                   move="intit",ck=0)
    isVisited.clear()

    startTime = time.time()
    print("DLS running......")
    nd = DLS(tmpNode,cutOffNode,limit)
    print("End of DLS...........")
    elapsedTime = time.time() - startTime
    if nd == None:
        print("Not found AC state.....")
        file.write("Not found AC state.....\n")
        file.write("Total call: " + str(call) + "\nTotal node Create: " + str(indx) + "\nElapsed Time : " + str(
            elapsedTime) + "\n")
    elif nd == cutOffNode:
        print("CutOff occured.....")
        file.write("CutOff occured..... \nNot found AC state.\n")
        file.write("Total call: " + str(call) + "\nTotal node Create: " + str(indx) + "\nElapsed Time : " + str(
            elapsedTime) + "\n")
    else:
        # print(nd.depth, call, indx)
        print("Found AC state")
        file.write("Depth is: " + str(nd.depth) + "\nTotal call: " + str(call) + "\nTotal node Create: " + str(
            indx) + "\nElapsed Time : " + str(elapsedTime) + "\n\n")
        answer = []
        tmpnd = copy.deepcopy(nd)

        while tmpnd.parent != -1:
            answer += [tmpnd]
            tmpnd = Node[tmpnd.parent]
        answer.reverse()
        for nn in answer:
            file.write("move :" + nn.move + "\n")
            filePrint(file, nn.state)
        file.close()

def call_DLS_2(tmpState,cutOffNode,limit):

    mp.clear()
    global indx
    indx = 0
    tmp = listToString(tmpState.copy())
    mp[tmp] = indx
    indx += 1
    global Node
    Node = []

    tmpNode = node(state=tmpState, parent=-1, action=getAction(srtX, srtY), g_cost=0, depth=0, h_cost=0, x=srtX, y=srtY,
                   move="intit",ck=0)
    Node += [tmpNode]

    isVisited.clear()

    nd = DLS(tmpNode, cutOffNode, limit)
    return nd,indx


def call_IDS(tmpState):
    file = open("output_IDS.txt", "w")

    # prntState(tmpState)
    file.write("Initial state :\n")
    filePrint(file, tmpState)
    global call
    call = 0

    nodeCount = 0
    cutOffNode = node(state=tmpState, parent=-5, action=getAction(srtX, srtY), g_cost=-1, depth=-1, h_cost=-1, x=srtX,
                      y=srtY,
                      move="intit",ck=0)
    print("IDS running......")
    startTime = time.time()

    for depthh in range(0,100):
        nd,tt=call_DLS_2(tmpState,cutOffNode,depthh)

        nodeCount+=tt

        if nd == None:
            print("End of DLS...........")
            elapsedTime = time.time() - startTime

            print("Not found AC state.....")
            file.write("Not found AC state.....\n")
            file.write("Total call: " + str(call) + "\nTotal node Create: " + str(nodeCount) + "\nElapsed Time : " + str(
                elapsedTime) + "\n")
            break
        elif nd != cutOffNode:
            print("End of DLS...........")
            elapsedTime = time.time() - startTime

            print("Found AC state")
            file.write("Depth is: " + str(nd.depth) + "\nTotal call: " + str(call) + "\nTotal node Create: " + str(
                nodeCount) +"\nLimit is : "+str(depthh)+ "\nElapsed Time : " + str(elapsedTime) + "\n\n")
            answer = []
            tmpnd = copy.deepcopy(nd)

            while tmpnd.parent != -1:
                answer += [tmpnd]
                tmpnd = Node[tmpnd.parent]
            answer.reverse()
            for nn in answer:
                file.write("move :" + nn.move + "\n")
                filePrint(file, nn.state)
            file.close()
            break
def call_GBFS(tmpState,chk):
    file = open("output_GBFS.txt", "w")

    # prntState(tmpState)
    file.write("Initial state :\n")
    filePrint(file, tmpState)

    mp.clear()
    global indx
    indx = 0
    tmp = listToString(tmpState.copy())
    mp[tmp] = indx
    indx += 1
    global Node
    Node = []
    global call
    call = 0

    cost=heuristic(tmpState,chk)

    tmpNode = node(state=tmpState, parent=-1, action=getAction(srtX, srtY), g_cost=0, depth=0, h_cost=cost, x=srtX, y=srtY,
                   move="intit",ck=1)
    Node += [tmpNode]
    isVisited.clear()

    startTime = time.time()
    print("GBFS running......")
    nd = GBFS(tmpNode,chk)
    print("End of GBFS...........")
    elapsedTime = time.time() - startTime
    if nd == None:
        print("Not found AC state.....")
        file.write("Not found AC state.....\n")
        file.write("Total call: " + str(call) + "\nTotal node Create: " + str(indx) + "\nElapsed Time : " + str(
            elapsedTime) + "\n")
    else:
        # print(nd.depth, call, indx)
        print("Found AC state")
        file.write("Depth is: " + str(nd.depth) + "\nTotal call: " + str(call) + "\nTotal node Create: " + str(
            indx) + "\nElapsed Time : " + str(elapsedTime) + "\n\n")
        answer = []
        tmpnd = copy.deepcopy(nd)

        while tmpnd.parent != -1:
            answer += [tmpnd]
            tmpnd = Node[tmpnd.parent]
        answer.reverse()
        for nn in answer:
            file.write("move :" + nn.move + "\n")
            filePrint(file, nn.state)
        file.close()

def call_A_star(tmpState,chk):
    file = open("output_A_star.txt", "w")

    file.write("Initial state :\n")
    filePrint(file, tmpState)

    mp.clear()
    global indx
    indx = 0
    tmp = listToString(tmpState.copy())
    mp[tmp] = indx
    indx += 1
    global Node
    Node = []
    global call
    call = 0

    cost = heuristic(tmpState, chk)

    tmpNode = node(state=tmpState, parent=-1, action=getAction(srtX, srtY), g_cost=0, depth=0, h_cost=cost, x=srtX,
                   y=srtY,
                   move="intit", ck=2)
    Node += [tmpNode]
    isVisited.clear()

    startTime = time.time()
    print("A* running......")
    nd = A_star(tmpNode, chk)
    print("End of A*...........")
    elapsedTime = time.time() - startTime
    if nd == None:
        print("Not found AC state.....")
        file.write("Not found AC state.....\n")
        file.write("Total call: " + str(call) + "\nTotal node Create: " + str(indx) + "\nElapsed Time : " + str(
            elapsedTime) + "\n")
    else:
        # print(nd.depth, call, indx)
        print("Found AC state")
        file.write("Depth is: " + str(nd.depth) + "\nTotal call: " + str(call) + "\nTotal node Create: " + str(
            indx) + "\nElapsed Time : " + str(elapsedTime) + "\n\n")
        answer = []
        tmpnd = copy.deepcopy(nd)

        while tmpnd.parent != -1:
            answer += [tmpnd]
            tmpnd = Node[tmpnd.parent]
        answer.reverse()
        for nn in answer:
            file.write("move :" + nn.move + "\n")
            filePrint(file, nn.state)
        file.close()
while True:

    # nPuzzle= int(input("Enter number n (of n-puzzle): "))
    #
    # row = column = round(math.sqrt(nPuzzle+1))
    #
    # acState = [[0 for i in range(column)] for j in range(row)]
    # initAcState(acState)
    #
    # print("Enter initial configuration :")
    # tmpState = [[0 for i in range(column)] for j in range(row)]
    # for i in range(row):
    #     for j in range(column):
    #         val = int(input("Enter value of <"+str(i+1)+","+str(j+1)+">: "))
    #         tmpState[i][j]= val
    #         if val ==0:
    #             srtX = i
    #             srtY = j

    with open("in.txt") as f:
        print("Enter number n (of n-puzzle): ")
        inn=[int(x) for x in next(f).split()]
        nPuzzle = inn[0]
        print(nPuzzle)
        row = column = round(math.sqrt(nPuzzle + 1))
        acState = [[0 for i in range(column)] for j in range(row)]
        initAcState(acState)
        print("Enter initial configuration :")
        tmpState = [[0 for i in range(column)] for j in range(row)]
        i = -1
        for line in f:
            i += 1
            j = -1
            for x in line.split():
                j += 1
                val = int(x)
                tmpState[i][j] = val
                if val ==0:
                    srtX = i
                    srtY = j
    prntState(tmpState)

    f.close()

    print("\n---------MENU-------------")
    print("Enter your choice : ")
    print("1.BFS\n2.UCS\n3.DLS\n4.IDS\n5.GBFS\n6.A*\n7.RUN ALL")

    choice = int(input())
    if choice==1:
        call_BFS(tmpState)
    elif choice == 2:
        call_UCS(tmpState)
    elif choice == 3:
        print("Enter Limit for DLS: ")
        limit = int(input())
        call_DLS(tmpState,limit)
    elif choice == 4:
        call_IDS(tmpState)
    elif choice == 5:
        print("Enter heuristic Choice:\n1.Misplaced tiles\n2.Manhattan distance")
        ch = int(input())
        call_GBFS(tmpState,ch)
    elif choice == 6:
        print("Enter heuristic Choice:\n1.Misplaced tiles\n2.Manhattan distance")
        ch = int(input())
        call_A_star(tmpState, ch)
    elif choice == 7:

        print("Enter Limit for DLS: ")
        limit = int(input())

        print("Enter heuristic Choice:\n1.Misplaced tiles\n2.Manhattan distance")
        ch = int(input())

        call_BFS(tmpState)
        call_UCS(tmpState)
        call_DLS(tmpState, limit)
        call_IDS(tmpState)
        call_GBFS(tmpState, ch)
        call_A_star(tmpState, ch)



    print("\nDO you want to continue from beginning?\n1.YES\n2.NO")

    deci=int(input())
    if deci ==2:
        exit()