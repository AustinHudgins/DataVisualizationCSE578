import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

dbfile = r"C:\Users\Austi\Git\DataVisualizationCSE578\Assignments\dinofunworld.db"




# Create a SQL connection to our SQLite database    
con = sqlite3.connect(dbfile)

cur = con.cursor()
def findingDist(): 
    visitorIDandsequences = []
    for row in cur.execute("SELECT visitorID, sequence FROM sequences where visitorID IN (165316, 1835254, 296394, 404385, 448990)"):
        squence = row[1]
        splitsquence = squence.split("-")
        visitorIDandsequences.append([row[0],splitsquence])

    manuStats = pd.DataFrame.from_records(visitorIDandsequences, columns=['visitorID', 'sequence'])
    distanceDict = {}
    for x in manuStats['visitorID']:
        distanceDict[x] = {}
    print(distanceDict)
    count = 0
    othercount= 0
    for x in distanceDict:
        for y in distanceDict:
            distance = 0
            for z, q in zip(manuStats['sequence'][count], manuStats['sequence'][othercount]):
                if (int(z) != int(q)):
                    distance += 1
            distanceDict[x][y] = distance
            othercount += 1
        count += 1
        othercount= 0

    print(distanceDict)

ridesID = []
ridesNames = []
for row in cur.execute("select attractionid, name from attraction where category LIKE '%rides%'"):
    ridesID.append(row[0])
    ridesNames.append(row[1])

sequences = []
for row in cur.execute("select visitorid, sequence from sequences"):
    squence = row[1]
    splitsquence = squence.split("-")
    sequences.append([row[0],splitsquence])

squencesData = pd.DataFrame.from_records(sequences, columns=['ID', 'sequence'])

ridesID2 = ridesID
MinMaxAvg = []

dict = {}
for name in ridesNames:
    dict[name] = {}

for i in range(len(ridesID)):
        squencesData['sequenceZeroandOnes'] = squencesData['sequence'].apply(lambda v: [1 if j == str(ridesID[i]) else 0 for j in v])
        count = np.sum(squencesData['sequenceZeroandOnes'].values.tolist(), axis=0)
        nonZeroCount = count[np.nonzero(count)]
        min = np.min(nonZeroCount)
        max = np.max(nonZeroCount)
        avg = (sum(count)/ len(count))
        #avg = np.round(avg)
        dict[ridesNames[i]] = {'min' : min,'max' : max,'avg' : avg  }
        MinMaxAvg.append([ridesNames[i], min, avg, max])
        
NameMinMaxAvgData = pd.DataFrame(MinMaxAvg, columns = ['Name', 'Min', 'Max', 'Avg'])
MinMaxAvgData = NameMinMaxAvgData.drop(['Name'], axis=1)
# pd.plotting.parallel_coordinates(NameMinMaxAvgData, class_column='Name')
# plt.gca().legend(bbox_to_anchor=(1.05, 1.0), loc='upper right')
# plt.title('Ride Attendance - Minimum, Maximum, Average')
# plt.ylabel('Attendance')
# plt.show()


pd.plotting.scatter_matrix(MinMaxAvgData)
plt.title('Scatterplot Matrix - Minimum, Maximum, Average Attendance')
plt.show()

# print(dict)

# Be sure to close the connection
con.close()
                   
