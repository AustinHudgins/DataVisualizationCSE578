import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

dbfile = r"C:\Users\Austi\Git\DataVisualizationCSE578\Assignments\dinofunworld.db"




# Create a SQL connection to our SQLite database    
con = sqlite3.connect(dbfile)

cur = con.cursor()

#Pie Chart 1 -  A pie chart depicting visits to thrill ride attractions.
def pyChart():
    thrillRidesAndVisits = []
    for row in cur.execute("SELECT attraction.name, COUNT(*) FROM checkin, attraction WHERE category LIKE '%thrill rides%' AND  checkin.attraction = attraction.attractionid GROUP BY attraction.name"):
        thrillRidesAndVisits.append(row)
    print(thrillRidesAndVisits)

    rideLabels = []
    rideVisits = []
    for ride in thrillRidesAndVisits:
        rideLabels.append(ride[0])
    rideVisits.append(ride[1])

    manuStats = pd.DataFrame.from_records(thrillRidesAndVisits, columns=['Rides','Visists'])

    plt.pie(manuStats['Visists'], labels=manuStats['Rides'],shadow=False)		
    plt.title("Visits to Thrill Ride attractions")
    plt.axis("equal")
    
def barchart():
    foodAndVisits = []
    for row in cur.execute("SELECT attraction.name, COUNT(*) FROM checkin, attraction WHERE category LIKE '%food%' AND  checkin.attraction = attraction.attractionid GROUP BY attraction.name"):
        foodAndVisits.append(row)
    print(foodAndVisits)

    manuStats = pd.DataFrame.from_records(foodAndVisits, columns=['Food','Visists'])
    #https://stackoverflow.com/questions/58814857/conversionerror-failed-to-convert-values-to-axis-units
    #plt.bar(range(len(manuStats['Visists'])), manuStats['Visists'] )	
    plt.bar(manuStats['Food'], manuStats['Visists'])
    #https://stackoverflow.com/questions/43618423/even-spacing-of-rotated-axis-labels-in-matplotlib-and-or-seaborn	
    plt.xticks(rotation =45, ha = "right")
    plt.xlabel("Food Stalls")
    plt.ylabel("Number of Visits")
    plt.title("Total Visits to Food Stalls")


def linegraph():
    for row in cur.execute("SELECT attractionId FROM attraction where attraction.Name = 'Atmosfear'"):
        attractionID = row[0]
    visitorIDandsequences = []
    for row in cur.execute("SELECT visitorID, sequence FROM sequences where sequence LIKE '%" + str(attractionID) + "%'"):
        squence = row[1]
        splitsquence = squence.split("-")
        first196splitsquence = splitsquence[:192]
        for i in range(0, len(first196splitsquence)):
            first196splitsquence[i] = int(first196splitsquence[i])
            if (first196splitsquence[i] == int(attractionID)):
                first196splitsquence[i] = 1
            else:
                first196splitsquence[i] = 0
        visitorIDandsequences.append([row[0],first196splitsquence])

    manuStats = pd.DataFrame.from_records(visitorIDandsequences, columns=['visitor', 'sequence'])

    visitors = np.sum(manuStats['sequence'].values.tolist(), axis=0)

    every5mins = range(0, len(visitors)*5, 5)

    plt.plot(every5mins, visitors)
    plt.ylabel('Number of visits')
    plt.xlabel('Time in minutes')
    plt.title('Attendance at Atmosfear every 5 minutes')
    plt.show()
    result = [[every5mins[i], visitors[i]] for i in range(len(visitors))]
    print(result)

kiddieRidesVisits = []
for row in cur.execute("SELECT count(checkin.visitorId) as COUNT FROM checkin LEFT JOIN attraction ON checkin.attraction = attraction.AttractionID WHERE attraction.Category LIKE '%kiddie%' GROUP BY attraction.Name ORDER BY COUNT"):
    kiddieRidesVisits.append(row)

manuStats = pd.DataFrame.from_records(kiddieRidesVisits, columns=['visits'])
visitsSorted = []
for ride in kiddieRidesVisits:
 visitsSorted.append(ride[0])

plt.boxplot(manuStats['visits'])
plt.title('Total visits to rides in the Kiddie Rides category')
plt.xlabel('Attraction')
plt.ylabel('Visitor Count')
plt.show()
print(visitsSorted)
# # Be sure to close the connection
con.close()
                   
