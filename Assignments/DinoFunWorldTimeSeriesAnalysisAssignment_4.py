import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

dbfile = r"C:\Users\Austi\Git\DataVisualizationCSE578\Assignments\dinofunworld.db"




# Create a SQL connection to our SQLite database    
con = sqlite3.connect(dbfile)

cur = con.cursor()
for row in cur.execute("SELECT attractionId FROM attraction where attraction.Name = 'Atmosfear'"):
    attractionID = row[0]

visitorIDandsequences = []
for row in cur.execute("SELECT visitorID, sequence FROM sequences where sequence LIKE '%" + str(attractionID) + "%'"):
    squence = row[1]
    splitsquence = squence.split("-")
    visitorIDandsequences.append([row[0],splitsquence])

squencesData = pd.DataFrame.from_records(visitorIDandsequences, columns=['visitorID', 'sequence'])
squencesData['sequence'] = squencesData['sequence'].apply(lambda v: [1 if j == str(attractionID) else 0 for j in v])

totalVisits = np.sum(squencesData['sequence'].values.tolist(), axis=0)

avg = np.mean(totalVisits)
std = np.nanstd(totalVisits)

anwser = [avg,std]

plt.ylabel('Attendance')
plt.xlabel('Time in minutes')
plt.title('Control Chart of attendance at Atmosfear')

plt.plot(range(0,len(totalVisits)), totalVisits, 'b-')
plt.plot([0,len(totalVisits)], [avg,avg], 'g-')
plt.plot([0,len(totalVisits)], [avg+std, avg+std], 'y-')
plt.plot([0,len(totalVisits)], [avg+2*std, avg+2*std], 'r-')
plt.plot([0,len(totalVisits)], [avg-std, avg-std], 'y-')
plt.plot([0,len(totalVisits)], [avg-2*std, avg-2*std], 'r-')

plt.gca().legend(('TotalAttendace','avg','std','2*std'),bbox_to_anchor=(1.05, 1.0), loc='upper right')

plt.show()

print(anwser)

window_size= 50
plt.plot(np.convolve(totalVisits, np.ones(window_size,)/window_size, 'same'), )
plt.ylabel('Attendance')
plt.xlabel('Time in minutes')
plt.title('Moving Average Chart of attendance at Atmosfear')
plt.show()


span = 50
df = pd.DataFrame({'totalVisits' : totalVisits})
df_exp = df.ewm(span=span).mean()
plt.plot(df_exp)
plt.ylabel('Attendance')
plt.xlabel('Time in minutes')
plt.title('Exponentially Weighted Moving Average Chart of the attendance at Atmosfear')
plt.show()
# Be sure to close the connection
con.close()
                   
