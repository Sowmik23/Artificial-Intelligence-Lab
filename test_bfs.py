
class Node():
	def __init__(self, state, parent, action, length, step_cost, cost, heuristic_cost):
		self.state = state
		self.parent = parent
		self.action = action
		self.length = length
		self.step_cost = step_cost
		self.cost = cost
		self.heuristic_cost = heuristic_cost

		self.up = None
		self.down = None
		self.right = None
		self.left = None

	def move_up(self):
		index_0 = [i[0] for i in np.where(self.state==0)]
		
		if index_0[1] == 2:
			return False
		else:
			print(index_0)
			print("this is test")
			new_state = self.state.copy()
			down_value = self.state[index_0[0],index_0[1]+1]
			
			new_state[index_0[0], index_0[1]] = down_value
			new_state[index_0[0], index_0[1]+1] = 0
			return new_state, down_value

	def move_left(self):
		index_0 = [i[0] for i in np.where(self.state==0)]
		
		if index_0[0] == 2:
			return False
		else:
			print(index_0)
			print("this is test")
			new_state = self.state.copy()
			right_value = self.state[index_0[0]+1, index_0[1]]
			
			new_state[index_0[0], index_0[1]] = right_value
			new_state[index_0[0]+1, index_0[1]] = 0
			return new_state, right_value

	def move_down(self):
		index_0 = [i[0] for i in np.where(self.state==0)]
		
		if index_0[1] == 0:
			return False
		else:
			print(index_0)
			print("this is test")
			new_state = self.state.copy()
			up_value = self.state[index_0[0], index_0[1]-1]
			
			new_state[index_0[0], index_0[1]] = up_value
			new_state[index_0[0], index_0[1]-1] = 0
			return new_state, up_value

	def move_right(self):
		index_0 = [i[0] for i in np.where(self.state==0)]
		print(index_0)
		print("this is test")
		if index_0[0] == 0:
			return False
		else:
			print(index_0)
			print("this is test")
			new_state = self.state.copy()
			left_value = self.state[index_0[0]-1, index_0[1]]
			
			new_state[index_0[0], index_0[1]] = left_value
			new_state[index_0[0]-1, index_0[1]] = 0
			return new_state, left_value

	#specific heuristic cost
	def Heuristic_cost(self, new_state, final, h_function, cost, length):
		if h_function == 'num_misplaced':
			return self.h_misplaced_cost(new_state, final)
		elif h_function == 'manhattan':
			return self.h_manhattan_cost(new_state, final)
		elif h_function == 'fair_manhattan':
			return self.h_manhattan_cost(new_state, final) - cost + length

	def h_misplaced_cost(self, new_state, final):
		cost = np.sum(new_state != final)-1  #as empty tiles can not be count
		if cost > 0:
			return cost
		else:
			return 0

	def h_manhattan_cost(self, new_state, final):
		current = new_state
		final_position_dictionary = {
			1: (0,0),
			2: (0,1),
			3: (0,2),
			5: (1,0),
			8: (1,1),
			6: (1,2),
			0: (2,0),
			7: (2,1),
			4: (2,2)
		}
		total = 0
		for i in range(3):
			for j in range(3):
				if current[i,j] !=0:
					total += sum(abs(x-y) for x,y in zip((i,j), final_position_dictionary[current[i,j]]))

		return total


	def print_path(self):
		state = [self.state]
		action = [self.action]
		length = [self.length]
		step_cost = [self.step_cost]
		cost = [self.cost]
		heuristic_cost = [self.heuristic_cost]

		while self.parent:
			# print("ablol tabol")
			self = self.parent
			state.append(self.state)
			action.append(self.action)
			length.append(self.length)
			step_cost.append(self.step_cost)
			cost.append(self.cost)
			heuristic_cost.append(self.heuristic_cost)

		cnt = 0
		while state:
			print('step {}'.format(cnt))
			print('action = {} depth= {} replaced tiles= {} total_cost= {}'.format(action.pop(), str(length.pop()), str(step_cost.pop()), str( cost.pop() + heuristic_cost.pop()) ))
			print(state.pop())
			print("\n\n")
			# print(cnt)
			cnt +=1



	# Breadth First Search
	def BFS(self, final):
		start_time = time.time()

		cnt=0
		visited = set([])
		q = [self]
		print(q)
		n = 0   #number of nodes poped
		ln = 1  #mx length of queue
		q_len = [0] #node depth
		cost = [0] #path cost
		# print(n)
		while q:
			# cnt+=1
			# if cnt==11:
			# 	break
			# if n > 100:
			# 	break
			# print("checking....")
			if len(q) > ln:
				ln = len(q)

			top = q.pop(0)
			n +=1

			current_len = q_len.pop(0)
			current_cost = cost.pop(0)
			print("Current node depth "+ str(current_len))
			print("Call Count "+str(n))

			visited.add(tuple(top.state.reshape(1,9)[0]))

			if np.array_equal(top.state, final):
				top.print_path()
				print("Total time to complete: %lfs" %(time.time()-start_time))
				return True
			
			else:
				# print("ok. aj r lagbe na.")
				if top.move_up():
					new_state, down_value = top.move_up()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
						top.up = Node(state = new_state, parent = top, action ='right', length = current_len + 1, step_cost=down_value, cost = current_cost + down_value, heuristic_cost = 0)
						q.append(top.up)
						q_len.append(current_len + 1)
						cost.append(current_cost + down_value)
						print("Exploring action up")

				if top.move_left():
					new_state, right_value = top.move_left()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
						top.left = Node(state = new_state, parent = top, action = 'down', length = current_len + 1, step_cost = right_value , cost = current_cost + right_value, heuristic_cost = 0)
						q.append(top.left)
						q_len.append(current_len + 1)
						cost.append(current_cost + right_value)
						print("Exploring action left")

				if top.move_down():
					new_state, up_value = top.move_down()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
						top.down = Node(state = new_state, parent = top, action ='left', length = current_len + 1, step_cost=up_value, cost = current_cost + up_value, heuristic_cost = 0)
						q.append(top.down)
						q_len.append(current_len + 1)
						cost.append(current_cost + up_value)
						print("Exploring action down")
				
				if top.move_right():
					new_state, left_value = top.move_right()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
						top.right = Node(state = new_state, parent = top, action = 'up', length = current_len + 1, step_cost = left_value , cost = current_cost + left_value, heuristic_cost = 0)
						q.append(top.right)
						q_len.append(current_len + 1)
						cost.append(current_cost + left_value)
						print("Exploring action right")
				print("Extracted node state: {}".format(new_state))



	# Iterative Depening Depth First Search
	def IDS(self, final_state):
		start_time = time.time()
		n = 0   #number of nodes poped
		ln = 1  #mx length of queue

		for i in range(20):
			q = [self]
			visited = set([])
			cost = [0]
			q_len = [0]

			while q:
				if len(q) > ln:
					ln = len(q)

				top = q.pop(0)
				n +=1
				current_len = q_len.pop(0)
				current_cost = cost.pop(0)
				print("Current node depth "+ str(current_len))
				print("Call Count "+str(n))

				visited.add(tuple(top.state.reshape(1,9)[0]))
				if np.array_equal(top.state, final_state):
					top.print_path()
					print("Total time to complete: %lfs" %(time.time()-start_time))
					return True

				else:
					if current_len < i:
						if top.move_up():
							print("Exploring action up")
							new_state, down_value = top.move_up()
							if tuple(new_state.reshape(1,9)[0]) not in visited:
								top.up = Node(state = new_state, parent = top, action = 'up', length= current_len + 1, step_cost=down_value, cost = current_cost + down_value, heuristic_cost = 0)
								q.insert(0, top.up)
								q_len.insert(0, current_len + 1)
								cost.insert(0, cost + down_value)

						if top.move_left():
							print("Exploring action left")
							new_state, right_value = top.move_left()
							if tuple(new_state.reshape(1,9)[0]) not in visited:
								top.left = Node(state = new_state, parent = top, action = 'left', length= current_len + 1, step_cost=right_value, cost = current_cost + right_value, heuristic_cost = 0)
								q.insert(0, top.left)
								q_len.insert(0, current_len + 1)
								cost.insert(0, cost + right_value)

						if top.move_down():
							print("Exploring action down")
							new_state, up_value = top.move_down()
							if tuple(new_state.reshape(1,9)[0]) not in visited:
								top.down = Node(state = new_state, parent = top, action = 'down', length= current_len + 1, step_cost=up_value, cost = current_cost + up_value, heuristic_cost = 0)
								q.insert(0, top.down)
								q_len.insert(0, current_len + 1)
								cost.insert(0, cost + up_value)

						if top.move_right():
							print("Exploring action right")
							new_state, left_value = top.move_right()
							if tuple(new_state.reshape(1,9)[0]) not in visited:
								top.right = Node(state = new_state, parent = top, action = 'right', length= current_len + 1, step_cost=left_value, cost = current_cost + left_value, heuristic_cost = 0)
								q.insert(0, top.right)
								q_len.insert(0, current_len + 1)
								cost.insert(0, cost + left_value)



	# Uniform Cost search
	def UCS(self, final_state):
		start_time = time.time()

		visited = set([])
		q = [(self,0)]
		n = 0 #number of nodes poped
		ln = 1 #max len of queue

		cost = [0]
		q_len = [(0, 0)]  #node depth(depth,cost)
		print("starting............")

		while q:
			q = sorted(q, key = lambda  x: x[1])
			# q_len = sorted(q_len, key = lambda x: x[1])
			q_len = sorted(q_len, key=itemgetter(0), reverse=False)
			
			cost = sorted(cost, key = lambda x: x)

			if len(q) > ln:
				ln = len(q)

			top = q.pop(0)[0]
			# print(top.state)

			n += 1
			current_len = q_len.pop(0)[0]
			current_cost = cost.pop(0)
			print("Current node depth "+ str(current_len))
			print("Call Count "+str(n))

			visited.add(tuple(top.state.reshape(1,9)[0]))

			if np.array_equal(top.state, final_state):
				top.print_path()
				print("Total time to complete: %lfs" %(time.time()-start_time))
				return True

			else:
				if top.move_up():
					print("Exploring action up")
					new_state, down_value = top.move_up()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
						top.up = Node(state = new_state, parent = top, action = 'up', length=current_len+1, step_cost = down_value, cost= current_cost+down_value,heuristic_cost = 0)
						q.append((top.up, current_cost + down_value))
						q_len.append((current_len+1, cost + down_value))
						cost.append(current_cost + down_value)

				if top.move_left():
					print("Exploring action left")
					new_state, right_value = top.move_left()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
						top.left = Node(state = new_state, parent = top, action = 'left', length=current_len+1,  step_cost = right_value, cost= current_cost+right_value,heuristic_cost = 0)
						q.append((top.left, current_cost + right_value))
						q_len.append((current_len+1, cost + right_value))
						cost.append(current_cost + right_value)

				if top.move_down():
					print("Exploring action down")
					new_state, up_value = top.move_down()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
						top.down = Node(state = new_state, parent = top, action = 'down', length=current_len+1, step_cost = up_value, cost= current_cost+up_value,heuristic_cost = 0)
						q.append((top.down, current_cost + up_value))
						q_len.append((current_len+1, cost + up_value))
						cost.append(current_cost + up_value)

				if top.move_right():
					print("Exploring action right")
					new_state, left_value = top.move_right()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
						top.right = Node(state = new_state, parent = top, action = 'right', length=current_len+1, step_cost = left_value, cost= current_cost+left_value,heuristic_cost = 0)
						q.append((top.right, current_cost + left_value))
						q_len.append((current_len+1, cost + left_value))
						cost.append(current_cost + left_value)



	# Best First Search
	def Best_FS(self, final_state):
		start_time = time.time()

		visited = set([])
		q = [(self,0)]
		n = 0 #number of nodes poped
		ln = 1 #max len of queue

		path_cost = [(0,0)]
		
		q_len = [(0, 0)]  #node depth(depth,cost)
		print("starting............")

		while q:
			q = sorted(q, key = lambda  x: x[1])
			# q_len = sorted(q_len, key = lambda x: x[1])
			q_len = sorted(q_len, key = lambda x: x[1])
			
			path_cost = sorted(path_cost, key = lambda x: x[1])

			if len(q) > ln:
				ln = len(q)

			top = q.pop(0)[0]
			# print(top.state)

			n += 1
			current_len = q_len.pop(0)[0]
			current_cost = path_cost.pop(0)[0]
			print("Current node depth "+ str(current_len))
			print("Call Count "+str(n))

			visited.add(tuple(top.state.reshape(1,9)[0]))

			if np.array_equal(top.state, final_state):
				top.print_path()
				print("Total time to complete: %lfs" %(time.time()-start_time))
				return True

			else:
				if top.move_up():
					print("Exploring action up")
					new_state, down_value = top.move_up()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
						heuristic_cost = self.h_misplaced_cost(new_state, final_state)
						top.up = Node(state = new_state, parent = top, action = 'up', length=current_len+1, step_cost = down_value, cost= current_cost+down_value,heuristic_cost = heuristic_cost)
						q.append((top.up, heuristic_cost))
						q_len.append((current_len+1, heuristic_cost))
						path_cost.append((current_cost + down_value, heuristic_cost))

				if top.move_left():
					print("Exploring action left")
					new_state, right_value = top.move_left()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
						heuristic_cost = self.h_misplaced_cost(new_state, final_state)
						top.left = Node(state = new_state, parent = top, action = 'left', length=current_len+1,  step_cost = right_value, cost= current_cost+right_value,heuristic_cost = heuristic_cost)
						q.append((top.left, heuristic_cost))
						q_len.append((current_len+1, heuristic_cost))
						path_cost.append((current_cost + right_value, heuristic_cost))

				if top.move_down():
					print("Exploring action down")
					new_state, up_value = top.move_down()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
						heuristic_cost = self.h_misplaced_cost(new_state, final_state)
						top.down = Node(state = new_state, parent = top, action = 'down', length=current_len+1, step_cost = up_value, cost= current_cost+up_value,heuristic_cost = heuristic_cost)
						q.append((top.down, heuristic_cost))
						q_len.append((current_len+1, heuristic_cost))
						path_cost.append((current_cost+up_value, heuristic_cost))

				if top.move_right():
					print("Exploring action right")
					new_state, left_value = top.move_right()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
						heuristic_cost = self.h_misplaced_cost(new_state, final_state)
						top.right = Node(state = new_state, parent = top, action = 'right', length=current_len+1, step_cost = left_value, cost= current_cost+left_value,heuristic_cost = heuristic_cost)
						q.append((top.right, heuristic_cost))
						q_len.append((current_len+1, heuristic_cost))
						path_cost.append((current_cost + left_value, heuristic_cost))




	def A_Star(self, final_state, h_function):
		start_time = time.time()

		visited = set([])
		q = [(self,0)]
		n = 0 #number of nodes poped
		ln = 1 #max len of queue

		path_cost = [(0,0)]
		q_len = [(0, 0)]  #node depth(depth,cost)

		print("starting............")

		while q:
			q = sorted(q, key = lambda  x: x[1])
			q_len = sorted(q_len, key = lambda x: x[1])
			path_cost = sorted(path_cost, key = lambda x: x[1])


			if len(q) > ln:
				ln = len(q)

			top = q.pop(0)[0]
			# print(top.state)

			n += 1
			current_len = q_len.pop(0)[0]
			current_cost = path_cost.pop(0)[0]
			print("Current node depth "+ str(current_len))
			print("Call Count "+str(n))

			visited.add(tuple(top.state.reshape(1,9)[0]))

			if np.array_equal(top.state, final_state):
				top.print_path()
				print("Total time to complete: %lfs" %(time.time()-start_time))
				return True

			else:
				if top.move_up():
					print("Exploring action up")
					new_state, down_value = top.move_up()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
						
						tmp = current_len + 1
						h_cost = self.Heuristic_cost(new_state, final_state, h_function, current_cost+down_value, tmp)
						
						total_cost = current_cost + down_value + h_cost
						top.up = Node(state = new_state, parent = top, action = 'up', length=tmp, step_cost = down_value, cost= current_cost + down_value, heuristic_cost = h_cost)
						q.append((top.up, total_cost))
						q_len.append((tmp, total_cost))
						path_cost.append((current_cost + down_value, total_cost))

				if top.move_left():
					print("Exploring action left")
					new_state, right_value = top.move_left()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
				
						tmp = current_len + 1
						h_cost = self.Heuristic_cost(new_state, final_state, h_function, current_cost+right_value, tmp)

						total_cost = current_cost+right_value + h_cost
						top.left = Node(state = new_state, parent = top, action = 'left', length=tmp, step_cost = right_value, cost= current_cost+right_value, heuristic_cost = h_cost)
						q.append((top.left, total_cost))
						q_len.append((tmp, total_cost))
						path_cost.append((current_cost+right_value, total_cost))

				if top.move_down():
					print("Exploring action down")
					new_state, up_value = top.move_down()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
					
						tmp = current_len + 1
						h_cost = self.Heuristic_cost(new_state, final_state, h_function, current_cost+up_value, tmp)

						total_cost = current_cost+up_value + h_cost
						top.down = Node(state = new_state, parent = top, action = 'down', length=tmp, step_cost = up_value, cost= current_cost+up_value, heuristic_cost = h_cost)
						q.append((top.down, total_cost))
						q_len.append((tmp, total_cost))
						path_cost.append((current_cost+up_value, total_cost))

				if top.move_right():
					print("Exploring action right")
					new_state, left_value = top.move_right()
					if tuple(new_state.reshape(1,9)[0]) not in visited:
			
						tmp = current_len + 1
						h_cost = self.Heuristic_cost(new_state, final_state, h_function, current_cost+left_value, tmp)

						total_cost = current_cost+left_value + h_cost
						top.right = Node(state = new_state, parent = top, action = 'right', length=tmp, step_cost = left_value, cost= current_cost+left_value, heuristic_cost = h_cost)
						q.append((top.right, total_cost))
						q_len.append((tmp, total_cost))
						path_cost.append((current_cost+left_value, total_cost))





if __name__ == '__main__':
	try:
	    import numpy as np
	    from operator import itemgetter
	    import time 

	except Exception as e:
		print("Some Modules are missing {}".format(e))


	else:
		# while True:
		# 	flag = 0
		# 	if flag == "1":
		# 		break	
		print("\nPlease, Select your option: \n")
		print("1. Testing mode\n2.Offline mode\n3.Exit")

		'''
			option = input(int);
			if option =="3":
				break

			if option=="1":
				while True:
					print("You choose Testing mode.\n")
					print("Give a number n:")
					n = input(int)
					print("You give {} Now select your option again\n".format(n))
					print("1.BFS\n2.UCS\n3.DLS\n4.IDS\n5.GBFS\n6.Back\n7.Exit")

					choice = input(int)
					print(choice)
					if choice == "6":
						break

					if choice == "7":
						flag = 1
						break
		'''
		# initial = np.array([1,2,3,5,6,0,7,8,4]).reshape(3,3)
		# final = np.array([1,2,3,4,5,6,7,8,0]).reshape(3,3)

		# initial = np.array([5,0,1,4,6,7,3,8,2]).reshape(3,3)
		# final = np.array([1,2,3,4,5,6,7,8,0]).reshape(3,3)

		initial = np.array([0,1,2,3,4,5,6,7,8]).reshape(3,3)
		final = np.array([5,1,0,4,6,7,3,8,2]).reshape(3,3)


		print("\nInitial state:\n")
		print(initial)

		print("\n\nFinal state:\n")
		print(final)

		print("\n**********<-Start->************\n")

		rn = Node(state=initial, parent=None, action=None, length=0, step_cost=0, cost=0, heuristic_cost=0)


		# rn.BFS(final)
		# print("hehehehehehehehe BFS finished!!!...........>")

		# hoy na
		# rn.UCS(final)
		# print("hehehehehehehehe UCS finished!!!...........>")

		# rn.IDS(final)
		# print("hehehehehehehehe IDS finished!!!...........>")

		# rn.Best_FS(final)
		# print("hehehehehehehehe Best_FS finished!!!...........>")

		# rn.A_Star(final, h_function='num_misplaced' )
		# print("hehehehehehehehe A_Star finished!!!...........>")

		rn.A_Star(final, h_function='manhattan' )
		print("hehehehehehehehe A_Star finished!!!...........>")

		'''
					if choice == "1":
						rn.BFS(final)
						print("hehehehehehehehe BFS finished!!!...........>")

					elif choice == '2':
						rn.UCS(final)
						print("hehehehehehehehe UCS finished!!!...........>")

					elif choice == '3':
						pass
					elif choice == '4':
						rn.IDS(final)
						print("hehehehehehehehe IDS finished!!!...........>")

					elif choice == '5':
						pass
					else:
						print("Please give number between 1 to 5")
						
			if flag == "1":
				break	

			elif option==2:
				print("You choose option 2")
			else:
				print("Please give number between 1 to 2")
		'''


	finally:
		print("\n\tGoog bye!!!\nSuccessfully end the program")







