import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


BFS = pd.read_csv("BFS.csv",na_values=["???","??? "])
Astar =pd.read_csv("A_star.csv",na_values=["???","??? "])


stepBFS = BFS['Memory (MB)'][40:len(BFS)]
stepAStar = Astar['Memory (MB)'][40:len(BFS)]


#stepBFS = BFS['Time (s)'][40:len(BFS)]
#stepAStar = Astar['Time (s)'][40:len(BFS)]

print(BFS)
# set width of bar
print(len(stepBFS))
barWidth = 0.25
fig = plt.subplots(figsize =(12, 8))

index = []
for i in range(0,len(stepBFS)):
        index.append(i+1)

# set height of bar
#IT = [12, 30, 1, 8, 22]
#ECE = [28, 6, 16, 5, 10]
#CSE = [29, 3, 24, 25, 17]
 
# Set position of bar on X axis
br1 = np.arange(len(stepBFS))
br2 = [x + barWidth for x in br1]
#br3 = [x + barWidth for x in br2]
 
# Make the plot
plt.bar(br1, stepBFS, color ='r', width = barWidth,
        edgecolor ='grey', label ='BFS')
plt.bar(br2, stepAStar, color ='g', width = barWidth,
        edgecolor ='grey', label ='A_star')
#plt.bar(br3, CSE, color ='b', width = barWidth,
#        edgecolor ='grey', label ='CSE')
 
# Adding Xticks
plt.xlabel('TC', fontweight ='bold', fontsize = 15)
plt.ylabel('MB', fontweight ='bold', fontsize = 15)
#plt.xticks([(r + barWidth) for r in range(len(IT))],
#        ['2015', '2016', '2017', '2018', '2019'])

plt.xticks([barWidth/2 + r for r in range(len(stepBFS))],index)
plt.title("The amount of memory used in MICRO COSMOS Testcases")
plt.legend()
plt.show()
