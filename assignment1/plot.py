import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
import numpy



BFS_depth = []
BFS_time = []
BFS_node = []

UCS_depth = []
UCS_time = []
UCS_node = []

DLS_depth = []
DLS_time = []
DLS_node = []

IDS_depth = []
IDS_time = []
IDS_node = []

GBFS_depth = []
GBFS_time = []
GBFS_node = []

A_star_depth = []
A_star_time = []
A_star_node = []




file = open("plot_data.txt","r")
j=1
while True:
    arr =[]
    ff= file.readline();

    if len(ff)==0:
        break
    if len(ff)>1 and j>2:
       	tmp= [i for i in ff.split('#')]
       	if tmp[1]=='bfs':
          val = int(tmp[2])
          if val<=20:
            BFS_depth.append(val)
            BFS_node.append(int(tmp[3]))
            BFS_time.append(int(float(tmp[4])))
       	elif tmp[1]=='ucs':
          val = int(tmp[2])
          if val<=20:
            UCS_depth.append(int(tmp[2]))
            UCS_node.append(int(tmp[3]))
            UCS_time.append(int(float(tmp[4])))
       	elif tmp[1]=='dls':
          val = int(tmp[2])
          if val<=20:
            DLS_depth.append(int(tmp[2]))
            DLS_node.append(int(tmp[3]))
            DLS_time.append(int(float(tmp[4])))
       	elif tmp[1]=='ids':
          val = int(tmp[2])
          if val<=20:
            IDS_depth.append(int(tmp[2]))
            IDS_node.append(int(tmp[3]))
            IDS_time.append(int(float(tmp[4])))
       	elif tmp[1]=='gbfs':
          val = int(tmp[2])
          if val<=20:
            GBFS_depth.append(int(tmp[2]))
            GBFS_node.append(int(tmp[3]))
            GBFS_time.append(int(float(tmp[4])))
       	elif tmp[1]=='a_star':
       		A_star_depth.append(int(tmp[2]))
       		A_star_node.append(int(tmp[3]))
       		A_star_time.append(int(float(tmp[4])))

    j+=1
file.close()

print(BFS_depth)
# print(BFS_node)
# print(BFS_time)

# BFS_depth.sort()

print(BFS_depth)


# plot line and give color for each line
plt.plot(BFS_depth,  color='red')
plt.plot(UCS_depth, color='green')
plt.plot(DLS_depth, color='orange')
plt.plot(IDS_depth, color='purple')
plt.plot(GBFS_depth, color='blue')
plt.plot(A_star_depth, color='cyan')


##path cost vs depth
# graph title
plt.title("Cost of algorithms")

# labels
plt.xlabel('Distance(initial-goal state)')
plt.ylabel('Path cost')
plt.xticks(numpy.arange(len(BFS_depth)), BFS_depth, rotation=0)
# plt.plot(numpy.arange(len(BFS_depth)), BFS_depth)

# legend
red_patch = mpatches.Patch(color='red', label='BFS')
green_patch = mpatches.Patch(color='green', label='UCS')
orange_patch = mpatches.Patch(color='orange', label='DLS')
purple_patch = mpatches.Patch(color='purple', label='IDS')
blue_patch = mpatches.Patch(color='blue', label='GBFS')
cyan_patch = mpatches.Patch(color='cyan', label='A*')

plt.legend(handles=[red_patch, green_patch, orange_patch, purple_patch, blue_patch, cyan_patch])

# add grid
plt.grid(True)

plt.show()



##Time vs depth
#plot time vs depth
plt.plot(BFS_time, color='red')
plt.plot(UCS_time, color='green')
plt.plot(DLS_time, color='orange')
plt.plot(IDS_time, color='purple')
plt.plot(GBFS_time, color='blue')
plt.plot(A_star_time, color='cyan')


# graph title
plt.title("Clock Time of algorithms")

# labels
plt.xlabel('Distance(initial-goal state)')
plt.ylabel('Time')
plt.xticks(numpy.arange(len(BFS_depth)), BFS_depth, rotation=0)

# legend
red_patch = mpatches.Patch(color='red', label='BFS')
green_patch = mpatches.Patch(color='green', label='UCS')
orange_patch = mpatches.Patch(color='orange', label='DLS')
purple_patch = mpatches.Patch(color='purple', label='IDS')
blue_patch = mpatches.Patch(color='blue', label='GBFS')
cyan_patch = mpatches.Patch(color='cyan', label='A*')

plt.legend(handles=[red_patch, green_patch, orange_patch, purple_patch, blue_patch, cyan_patch])

# add grid
plt.grid(True)

plt.show()


#plot node vs depth
plt.plot(BFS_node, color='red')
plt.plot(UCS_node, color='green')
plt.plot(DLS_node, color='orange')
plt.plot(IDS_node, color='purple')
plt.plot(GBFS_node, color='blue')
plt.plot(A_star_node, color='cyan')

# graph title
plt.title("Node created of algorithms")

# labels
plt.xlabel('Distance(initial-goal state)')
plt.ylabel('Number of Node created')
plt.xticks(numpy.arange(len(BFS_depth)), BFS_depth, rotation=0)

# legend
red_patch = mpatches.Patch(color='red', label='BFS')
green_patch = mpatches.Patch(color='green', label='UCS')
orange_patch = mpatches.Patch(color='orange', label='DLS')
purple_patch = mpatches.Patch(color='purple', label='IDS')
blue_patch = mpatches.Patch(color='blue', label='GBFS')
cyan_patch = mpatches.Patch(color='cyan', label='A*')

plt.legend(handles=[red_patch, green_patch, orange_patch, purple_patch, blue_patch, cyan_patch])

# add grid
plt.grid(True)

plt.show()




