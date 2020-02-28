class node():
    def __init__(self, state, parent, action, g_cost, depth, h_cost, x, y, move, check):
        self.state = state
        self.parent = parent
        self.action = action
        self.g_cost = g_cost
        self.depth = depth
        self.h_cost = h_cost
        self.x=x
        self.y=y
        self.move=move
        self.check=check

    def __lt__(self, other):
        if self.check == 0:
            return self.g_cost<other.g_cost
        elif self.check == 1:
                return self.h_cost<other.h_cost
        elif self.check == 2:
                return (self.h_cost+self.g_cost)<(other.h_cost+other.g_cost)



def storeData(my_list):
	print(my_list)
	with open('plot_data.txt', 'a') as f:
		for item in my_list:
			f.write("%s#" % item)
			if my_list.index(item)==4:
				f.write("\n")
	# f.close()




def initFinalState(acceptState, tmp):
	# print(tmp)
	cnt = 1
	row = len(acceptState)
	l = len(tmp)
	# for i in range(0, l):
	# 	print(tmp[i])
	k = 0
	for i in range(0,row):
	    for j in range(0,row):
	        acceptState[i][j]= tmp[k]
	        k+=1


def printState(state):
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
    limit = row-1
    result = []
    if x<limit:
        result+=["down"]
    if x>0:
        result+=["up"]
    if y<limit:
        result+=["right"]
    if y>0:
        result+=["left"]

    return result

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
    string =""
    for i in range(len(tmp)):
        for j in range(len(tmp)):
            string+=str(tmp[i][j])
            string+=' '
    return string

def heuristic(tmpState,check):
    row = len(tmpState)
    cnt = 0
    if check == 1:
        for i in range(0, row):
            for j in range(0, row):
                if (tmpState[i][j]!=acceptState[i][j]) and tmpState[i][j]!=0:
                    cnt+=1

    elif check == 2:
        mpp= collections.ChainMap()
        for i in range(0, row):
            for j in range(0, row):
                mpp[acceptState[i][j]]=[i,j]
        for i in range(0, row):
            for j in range(0, row):
                tmp = mpp[tmpState[i][j]]
                cnt+=(abs(i-tmp[0])+abs(j-tmp[1]))
    return cnt


def BFS(tmpState):
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
    tmpNode = node(state=tmpState, parent=-1, action=getAction(startX, startY), g_cost=0, depth=0, h_cost=0, x=startX, y=startY,move="intit",check=0)
    Node += [tmpNode]
    isVisited.clear()
    queuee = []
    queuee.append(tmpNode)
    isVisited[listToString(tmpNode.state)] = 1

    while len(queuee) !=0:
        nd = queuee.pop(0)
        x=nd.x
        y=nd.y
        call+=1
        if nd.state==acceptState:
            return nd
        for mov in nd.action:
            X,Y=movCheck(mov,x,y)
            nwstate = copy.deepcopy(nd.state)
            nwstate[x][y]=nd.state[X][Y]
            nwstate[X][Y] = nd.state[x][y]
            tmp=listToString(nwstate)
            nwNode = node(nwstate,mp[listToString(nd.state)],getAction(X,Y),nd.g_cost,nd.depth+1,nd.h_cost,X,Y,mov,0)
            if tmp not in mp:
                mp[tmp]=indx
                indx+=1
                Node+=[nwNode]
            if nwstate==acceptState:
                return nwNode

            if tmp not in isVisited:
                queuee.append(nwNode)
                isVisited[tmp] = 1
    return None

def BFS_print():
	file = open("1_BFS.txt", "w")
	file.write("Initial state :\n")
	filePrint(file, tmpState)

	startTime = time.time()
	print("BFS Running...")

	nd=BFS(tmpState)

	print("BFS Finished!")
	elapsedTime = time.time() - startTime

	if nd == None:
		print("No Aceepted state found!")
		file.write("No Aceepted state found!\n")
		file.write("Number of call: " + str(call) + "\nNumber of node created: " + str(indx) + "\nTime : " + str(elapsedTime) + "\n")
	else:
		print("Aceepted state found!")
		file.write("Depth: " + str(nd.depth) + "\nNumber of call: " + str(call) + "\nNumber of node created: " + str(indx) + "\nTime : " + str(elapsedTime) + "\n\n")
		answer = []
		tmpnd = copy.deepcopy(nd)
		while tmpnd.parent != -1:
			answer += [tmpnd]
			tmpnd = Node[tmpnd.parent]
		answer.reverse()
		for nn in answer:
			file.write("Current Move: " + nn.move + ", Current Depth: "+str(nn.depth)+"\n")
			filePrint(file, nn.state)
		file.close()
		D = nd.depth
		N = indx
		T = elapsedTime
		return D,N,T 



def UCS(tmpState):
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
    tmpNode = node(state=tmpState, parent=-1, action=getAction(startX, startY), g_cost=0, depth=0, h_cost=0, x=startX, y=startY, move="intit",check=0)
    Node += [tmpNode]
    isVisited.clear()
    q = queue.PriorityQueue()
    q.put(tmpNode)
    isVisited[listToString(tmpNode.state)] = 1

    while not q.empty():
        nd = q.get()
        x=nd.x
        y=nd.y
        call+=1
        isVisited[listToString(nd.state)] = 2
        if nd.state==acceptState:
            return nd
        for mov in nd.action:
            X,Y=movCheck(mov,x,y)
            nwstate = copy.deepcopy(nd.state)
            nwstate[x][y]=nd.state[X][Y]
            nwstate[X][Y] = nd.state[x][y]
            tmp=listToString(nwstate)
            nwNode = node(nwstate,mp[listToString(nd.state)],getAction(X,Y),nd.g_cost+1,nd.depth+1,nd.h_cost,X,Y,mov,0)
            if tmp not in mp:
                mp[tmp]=indx
                indx+=1
                Node+=[nwNode]

            if tmp not in isVisited:
                q.put(nwNode)
                isVisited[tmp] = 1
            elif isVisited[tmp]==1:
                q.put(nwNode)
    return None


def UCS_print():
	file = open("2_UCS.txt", "w")
	file.write("Initial state :\n")
	filePrint(file, tmpState)

	startTime = time.time()
	print("UCS Running...")
	nd=UCS(tmpState)
	print("UCS Finished!")
	elapsedTime = time.time() - startTime

	if nd == None:
		print("No Aceepted state found!")
		file.write("No Aceepted state found!\n")
		file.write("Number of call: " + str(call) + "\nNumber of node created: " + str(indx) + "\nTime : " + str(elapsedTime) + "\n")
	else:
		print("Aceepted state found!")
		file.write("Depth: " + str(nd.g_cost) + "\nNumber of call: " + str(call) + "\nNumber of node created: " + str(indx) + "\nTime : " + str(elapsedTime) + "\n\n")
		answer = []
		tmpnd = copy.deepcopy(nd)
	while tmpnd.parent != -1:
		answer += [tmpnd]
		tmpnd = Node[tmpnd.parent]
	answer.reverse()
	for nn in answer:
		file.write("Current Move: " + nn.move + ", Current Depth: "+str(nn.depth)+"\n")
		filePrint(file, nn.state)
	file.close()
	D = nd.depth
	N = indx
	T = elapsedTime
	return D,N,T 



def DLS(tmpNode,cutOffNode,limit):
    isVisited[listToString(tmpNode.state)] = 1

    nd = copy.deepcopy(tmpNode)
    x=nd.x
    y=nd.y
    global call
    call+=1
    if nd.state==acceptState:
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
        if nwstate==acceptState:
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



def DLS_print(tmpState,limit):
    file = open("3_DLS.txt", "w")
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
    tmpNode = node(state=tmpState, parent=-1, action=getAction(startX, startY), g_cost=0, depth=0, h_cost=0, x=startX, y=startY, move="intit",check=0)
    Node += [tmpNode]
    cutOffNode = node(state=tmpState, parent=-5, action=getAction(startX, startY), g_cost=-1, depth=-1, h_cost=-1, x=startX, y=startY, move="intit",check=0)
    isVisited.clear()

    startTime = time.time()
    print("DLS running...")
    nd = DLS(tmpNode,cutOffNode,limit)
    print("DLS Finished!")
    elapsedTime = time.time() - startTime
    if nd == None:
        print("No Aceepted state found!")
        file.write("No Aceepted state found!\n")
        file.write("Number of call: " + str(call) + "\nNumber of node created: " + str(indx) + "\nTime : " + str(
            elapsedTime) + "\n")
    elif nd == cutOffNode:
        print("CutOff occured.")
        file.write("CutOff occured. \nNo Aceepted state found!\n")
        file.write("Number of call: " + str(call) + "\nNumber of node created: " + str(indx) + "\nTime : " + str(elapsedTime) + "\n")
    else:
        print("Aceepted state found!")
        file.write("Depth: " + str(nd.depth) + "\nNumber of call: " + str(call) + "\nNumber of node created: " + str(indx) + "\nTime : " + str(elapsedTime) + "\n\n")
        answer = []
        tmpnd = copy.deepcopy(nd)

        while tmpnd.parent != -1:
            answer += [tmpnd]
            tmpnd = Node[tmpnd.parent]
        answer.reverse()
        for nn in answer:
            file.write("Current Move: " + nn.move + ", Current Depth: "+str(nn.depth)+"\n")
            filePrint(file, nn.state)
        file.close()
        D = nd.depth
        N = indx
        T = elapsedTime
    return D,N,T 




def IDS(tmpState,cutOffNode,limit):
    mp.clear()
    global indx
    indx = 0
    tmp = listToString(tmpState.copy())
    mp[tmp] = indx
    indx += 1
    global Node
    Node = []

    tmpNode = node(state=tmpState, parent=-1, action=getAction(startX, startY), g_cost=0, depth=0, h_cost=0, x=startX, y=startY, move="intit",check=0)
    Node += [tmpNode]
    isVisited.clear()
    nd = DLS(tmpNode, cutOffNode, limit)
    return nd,indx


def IDS_print(tmpState):
    file = open("4_IDS.txt", "w")

    file.write("Initial state :\n")
    filePrint(file, tmpState)
    global call
    call = 0

    nodeCount = 0
    cutOffNode = node(state=tmpState, parent=-5, action=getAction(startX, startY), g_cost=-1, depth=-1, h_cost=-1, x=startX, y=startY, move="intit",check=0)
    print("IDS running...")
    startTime = time.time()

    for depthh in range(0,100):
        nd,tt=IDS(tmpState,cutOffNode,depthh)

        nodeCount+=tt

        if nd == None:
            print("IDS Finished!")
            elapsedTime = time.time() - startTime

            print("No Aceepted state found!")
            file.write("No Aceepted state!\n")
            file.write("Number of call: " + str(call) + "\nNumber of node created: " + str(nodeCount) + "\nTime : " + str(
                elapsedTime) + "\n")
            break
        elif nd != cutOffNode:
            print("IDS Finished!")
            elapsedTime = time.time() - startTime

            print("Aceepted state found!")
            file.write("Depth: " + str(nd.depth) + "\nNumber of call: " + str(call) + "\nNumber of node created: " + str(nodeCount) +"\nLimit: "+str(depthh)+ "\nTime : " + str(elapsedTime) + "\n\n")
            answer = []
            tmpnd = copy.deepcopy(nd)

            while tmpnd.parent != -1:
                answer += [tmpnd]
                tmpnd = Node[tmpnd.parent]
            answer.reverse()
            for nn in answer:
                file.write("Current Move: " + nn.move + ", Current Depth: "+str(nn.depth)+"\n")
                filePrint(file, nn.state)
            file.close()
            D = nd.depth
            N = indx
            T = elapsedTime
            return D,N,T 
            # break



def GBFS(tmpState,chk):
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

    tmpNode = node(state=tmpState, parent=-1, action=getAction(startX, startY), g_cost=0, depth=0, h_cost=cost, x=startX, y=startY, move="intit",check=1)
    Node += [tmpNode]
    isVisited.clear()

    q = queue.PriorityQueue()
    q.put(tmpNode)
    isVisited[listToString(tmpNode.state)] = 1

    while not q.empty():
        nd = q.get()
        x=nd.x
        y=nd.y
        call+=1
        isVisited[listToString(nd.state)] = 2
        if nd.state==acceptState:
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
                mp[tmp] = indx
                indx += 1
                Node += [nwNode]

                q.put(nwNode)
                isVisited[tmp] = 1
    return None


def GBFS_print():
	file = open("5_GBFS.txt", "w")
	file.write("Initial state :\n")
	filePrint(file, tmpState)

	startTime = time.time()
	print("GBFS running...")
	
	print("Enter heuristic choice:\n1. Misplaced tiles\n2. Manhattan distance")
	ch = int(input())

	nd=GBFS(tmpState,ch)
	print("GBFS Finished!")

	elapsedTime = time.time() - startTime
	if nd == None:
		print("No Aceepted state found!")
		file.write("No Aceepted state found!\n")
		file.write("Number of call: " + str(call) + "\nNumber of node created: " + str(indx) + "\nTime : " + str(elapsedTime) + "\n")
	else:
		print("Aceepted state found!")
		file.write("Depth: " + str(nd.depth) + "\nNumber of call: " + str(call) + "\nNumber of node created: " + str(indx) + "\nTime : " + str(elapsedTime) + "\n\n")
		answer = []
		tmpnd = copy.deepcopy(nd)
	while tmpnd.parent != -1:
		answer += [tmpnd]
		tmpnd = Node[tmpnd.parent]
	answer.reverse()
	for nn in answer:
		file.write("Current Move: " + nn.move + ", Current Depth: "+str(nn.depth)+"\n")
		filePrint(file, nn.state)
	file.close()
	D = nd.depth
	N = indx
	T = elapsedTime
	return D,N,T 



def A_star(tmpState,chk):
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

    tmpNode = node(state=tmpState, parent=-1, action=getAction(startX, startY), g_cost=0, depth=0, h_cost=cost, x=startX, y=startY, move="intit", check=2)
    Node += [tmpNode]
    isVisited.clear()
    q = queue.PriorityQueue()
    q.put(tmpNode)
    isVisited[listToString(tmpNode.state)] = 1

    while not q.empty():
        nd = q.get()
        x=nd.x
        y=nd.y
        call+=1
        isVisited[listToString(nd.state)] = 2
        if nd.state==acceptState:
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
                mp[tmp] = indx
                indx += 1
                Node += [nwNode]

                q.put(nwNode)
                isVisited[tmp] = 1
    return None


def A_star_print():
	file = open("6_A_star.txt", "w")
	file.write("Initial state :\n")
	filePrint(file, tmpState)

	startTime = time.time()
	print("A* running...")
	
	print("Enter heuristic choice:\n1. Misplaced tiles\n2. Manhattan distance")
	ch = int(input())
	nd=A_star(tmpState, ch)

	print("A* Finished!")
	elapsedTime = time.time() - startTime

	if nd == None:
		print("No Aceepted state found!")
		file.write("No Aceepted state found!\n")
		file.write("Number of call: " + str(call) + "\nNumber of node created: " + str(indx) + "\nTime : " + str(elapsedTime) + "\n")
	else:
		print("Aceepted state found")
		file.write("Depth: " + str(nd.g_cost) + "\nNumber of call: " + str(call) + "\nNumber of node created: " + str(indx) + "\nTime : " + str(elapsedTime) + "\n\n")
		answer = []
		tmpnd = copy.deepcopy(nd)
	while tmpnd.parent != -1:
		answer += [tmpnd]
		tmpnd = Node[tmpnd.parent]
	answer.reverse()
	for nn in answer:
		file.write("Current Move: " + nn.move + ", Current Depth: "+str(nn.depth)+"\n")
		filePrint(file, nn.state)
	file.close()
	D = nd.depth
	N = indx
	T = elapsedTime
	return D,N,T 




if __name__ == '__main__':
	try:
	    import numpy as np
	    from operator import itemgetter
	    import time 
	    import math
	    import collections
	    import copy
	    import queue

	    Node = []
	    mp = collections.ChainMap()
	    indx = 0
	    isVisited = collections.ChainMap()
	    call = 0
	   
	except Exception as e:
		print("Some Modules are missing {}".format(e))

	else:
		# Take input n, initial and final state from input.txt file
		with open("input.txt") as file:
			print("Value of n is: ")

			n_input=[int(x) for x in next(file).split()]
			n = n_input[0]
			print(n)

			row = column = round(math.sqrt(n + 1))

			# acceptState = [[0 for i in range(column)] for j in range(row)]
			# initAcState(acceptState)

			print("Initial state :")
			tmpState = [[0 for i in range(column)] for j in range(row)]
			i = -1
			for line in file:
			    i += 1
			    if i==3:
			    	break
			    j = -1
			    for x in line.split():
			        j += 1
			        val = int(x)
			        tmpState[i][j] = val
			        if val ==0:
			            startX = i
			            startY = j

		printState(tmpState)
		file.close()

		tmp = []
		fp = open("input.txt")
		for i, line in enumerate(fp):
		    if i >= 5:
		        for x in line.split():
		        	# print(x)
		        	val = int(x)
		        	tmp.append(val)
		    
		fp.close()
		# print(tmp)
		print("Final State:")

		acceptState = [[0 for i in range(column)] for j in range(row)]
		initFinalState(acceptState,tmp)

		final =np.array(tmp).reshape(3,3)
		print(final)


		while True:
		    print("\nPlease, Select your option:")
		    print("\t1. Testing mode\n\t2. Offline mode\n\t3. Exit\n")

		    option = int(input())

		    if option==1:
		    	while True:
			    	print("\tSelect your algorithm to solve puzzle:")
			    	print("\t1. BFS\n\t2. UCS\n\t3. DLS\n\t4. IDS\n\t5. GBFS\n\t6. A*\n\t7. All(BFS, UCS, DLS, IDS, GBFS, A*)\n\t8. Back\n\t9. Exit")

			    	choice = int(input())

			    	if choice==8:
			    		break

			    	if choice==1:
			    		my_list = []
			    		my_list.append(n)

			    		D,N,T = BFS_print()

			    		my_list.append('bfs')
			    		my_list.append(D)
			    		my_list.append(N)
			    		my_list.append(T)

			    	elif choice == 2:
			    		my_list = []
			    		my_list.append(n)

			    		D,N,T = UCS_print()
			    		my_list.append('ucs')
			    		my_list.append(D)
			    		my_list.append(N)
			    		my_list.append(T)

			    	elif choice == 3:
			    		print("Enter Limit for DLS:\n")
			    		limit = int(input())
			    		my_list = []
			    		my_list.append(n)
			    		# startTime = time.time()
			    		D,N,T = DLS_print(tmpState,limit)
			    		my_list.append('dls')
			    		my_list.append(D)
			    		my_list.append(N)
			    		my_list.append(T)

			    	elif choice == 4:
			    		my_list = []
			    		my_list.append(n)

			    		D,N,T = IDS_print(tmpState)
			    		my_list.append('ids')
			    		my_list.append(D)
			    		my_list.append(N)
			    		my_list.append(T)

			    	elif choice == 5:
			    		my_list = []
			    		my_list.append(n)

			    		D,N,T = GBFS_print()
			    		my_list.append('gbfs')
			    		my_list.append(D)
			    		my_list.append(N)
			    		my_list.append(T)

			    	elif choice == 6:
			    		my_list = []
			    		my_list.append(n)

			    		D,N,T = A_star_print()
			    		my_list.append('a_star')
			    		my_list.append(D)
			    		my_list.append(N)
			    		my_list.append(T)

			    	elif choice == 7:
			    		print("Enter DLS LIMIT: ")
			    		DLS_limit = int(input())

			    		my_list = []
			    		my_list.append(n)

			    		D,N,T = BFS_print()
			    		my_list.append('bfs')
			    		my_list.append(D)
			    		my_list.append(N)
			    		my_list.append(T)
			    		storeData(my_list)

			    		my_list = []
			    		my_list.append(n)

			    		D,N,T = UCS_print()
			    		my_list.append('ucs')
			    		my_list.append(D)
			    		my_list.append(N)
			    		my_list.append(T)
			    		storeData(my_list)

			    		my_list = []
			    		my_list.append(n)
			    		D,N,T = DLS_print(tmpState,DLS_limit)
			    		my_list.append('dls')
			    		my_list.append(D)
			    		my_list.append(N)
			    		my_list.append(T)
			    		storeData(my_list)

			    		my_list = []
			    		my_list.append(n)

			    		D,N,T = IDS_print(tmpState)
			    		my_list.append('ids')
			    		my_list.append(D)
			    		my_list.append(N)
			    		my_list.append(T)
			    		storeData(my_list)

			    		my_list = []
			    		my_list.append(n)
			    		D,N,T = GBFS_print()

			    		my_list.append('gbfs')
			    		my_list.append(D)
			    		my_list.append(N)
			    		my_list.append(T)
			    		storeData(my_list)

			    		my_list = []
			    		my_list.append(n)

			    		D,N,T = A_star_print()
			    		my_list.append('a_star')
			    		my_list.append(D)
			    		my_list.append(N)
			    		my_list.append(T)
			    		storeData(my_list)



			    	elif choice ==9:
			    		exit()

			    	

		    elif option==2:
		    	print("Testing mode\n")

		    elif option==3:
		    	exit()

	finally:
		print("\n\tGoog bye!!!\nSuccessfully end the program")





