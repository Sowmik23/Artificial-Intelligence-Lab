import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
import numpy

# data
n = [2,3,8,12,15,18,20]
BFS = [3,4,5,6,7,5,4]
UCS = [9,7,6,8,5,4,3]
DLS = [6,5,4,7,6,3,2]
IDS = [7,4,2,6,9,8,1]
GBFS = [1,3,5,2,6,7,1]
A_star = [1,4,2,5,2,1,3]

# plot line and give color for each line
plt.plot(BFS, color='red')
plt.plot(UCS, color='green')
plt.plot(DLS, color='orange')
plt.plot(IDS, color='purple')
plt.plot(GBFS, color='blue')
plt.plot(A_star, color='cyan')


# graph title
plt.title("Time plot difference")

# labels
plt.xlabel('Value of n puzzle')
plt.ylabel('Time')
plt.xticks(numpy.arange(len(n)), n, rotation=90)

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














