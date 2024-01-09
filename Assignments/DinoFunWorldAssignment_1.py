import pandas as pd
import sqlite3

dbfile = r"C:\Users\Austi\Git\DataVisualizationCSE578\Assignments\dinofunworld.db"


# 3 Questions to Awnser:
# What is the most popular atraction to vist in the park?
# what ride (not that not all attractions are rides) has the second longest average visit time?
# Which Fast Food offering has the fewest vistiors?



# Common SQL commands I might need again: 
# SELECT column1, column2, ... FROM table_name;
# DISTINCT to get unquie values.

# Notes to self: 
# About question 1, How do we define popular? ( most checkins?)
# About question 2, remove all data with type not rides!
# About question 3, remove all data with type that is not Fast Food.    

# Create a SQL connection to our SQLite database    
con = sqlite3.connect(dbfile)

cur = con.cursor()

# Grab all Attractions 
allTypesOfAttractions= []
for row in cur.execute("SELECT DISTINCT type FROM attraction"):
    allTypesOfAttractions.append(row)

# Grab all Attractions that are rides
allRides= []
for row in cur.execute("SELECT AttractionID FROM attraction WHERE Category LIKE '%Ride%' "):
    allRides.append(row[0])

# Grab count of all attractions by ID
# https://stackoverflow.com/questions/19793189/get-count-for-each-distinct-value
attractionsAndNumberOfCheckins = []
for row in cur.execute("SELECT attraction, count(*) as 'num'  FROM checkin GROUP BY attraction"):
    attractionsAndNumberOfCheckins.append(row)

# Grab count of all food attractions by ID
# https://stackoverflow.com/questions/19793189/get-count-for-each-distinct-value
attractionsAndNumberOfCheckinsAtFood = []
for row in cur.execute("SELECT checkin.attraction, count(*) as 'num'  FROM checkin, attraction WHERE attraction.Category LIKE '%food%' GROUP BY attraction "):
    attractionsAndNumberOfCheckinsAtFood.append(row)
    print(attractionsAndNumberOfCheckinsAtFood)

# Rank attrations by what is most visted.
# https://stackoverflow.com/questions/31942169/python-sort-array-of-arrays-by-multiple-conditions
sorter = (lambda x : (x[1]))
rankedAttractionsIDs = sorted(attractionsAndNumberOfCheckins, key=sorter, reverse=True)

# Some of the ranked Attractions that might be used later.
mostPopularAttractionID = rankedAttractionsIDs[0][0]
leastPopularAttractionID = rankedAttractionsIDs[-1][0]
secondLeastPopularAttractionID = rankedAttractionsIDs[-2][0]

# Question 1 - Answer, most popular attraction to visit
# https://www.w3schools.com/sql/sql_where.asp
mostPopularAttractionArray = []
for row in cur.execute("SELECT Name FROM attraction WHERE AttractionID=" + str(mostPopularAttractionID)):
   mostPopularAttractionArray.append(row)
mostPopularAttraction = mostPopularAttractionArray[0][0]

# Question 2 - Second longest Avg visit time for a ride.
# https://www.w3schools.com/sql/sql_avg.asp


stringOfRides = ''
for ride in allRides:
    stringOfRides += (str(ride) + ",")
stringOfRides = stringOfRides[:-1]

arrayOfRides = stringOfRides.split(',')

def get_sec(time_str):
    # https://stackoverflow.com/questions/6402812/how-to-convert-an-hmmss-time-string-to-seconds-in-python
    try:
        h, m, s = time_str.split(':')
        return int(h) * 3600 + int(m) * 60 + int(s)
    except:
        print("cant split" + str(time_str) )

arrayOfRidesAndDuration = []

#avg(checkin.duration)

for row in cur.execute("SELECT attraction, duration FROM checkin WHERE attraction in (" + stringOfRides + ") AND duration IS NOT NULL"):
   arrayOfRidesAndDuration.append([row[0],get_sec(str(row[1]))])
sorter = (lambda x : (x[0]))
sortedArrayOfRidesAndDuration = sorted(arrayOfRidesAndDuration, key=sorter)

# Get Avg of all rides each
arrayOfRidesDurationAvgs = []
count = 0
sum = 0
currentNum = 0
first = True
for array in sortedArrayOfRidesAndDuration:
    if(first):
        arrayOfRidesDurationAvgs.append(array)
        first = False
        currentNum = array[0]
        sum += array[1]
        count += 1
    elif(currentNum == array[0]):
        sum += array[1]
        arrayOfRidesDurationAvgs[len(arrayOfRidesDurationAvgs) - 1][1] = sum
        count += 1
    elif(currentNum != array[0]):
        arrayOfRidesDurationAvgs[len(arrayOfRidesDurationAvgs) - 1][1] = round(sum/count, 3)
        arrayOfRidesDurationAvgs.append(array)
        count = 0
        sum = 0
        currentNum = array[0]
arrayOfRidesDurationAvgs[len(arrayOfRidesDurationAvgs) - 1][1] = round(sum/count, 3)

sorter = (lambda x : (x[1]))
arrayOfRidesDurationAvgsShortedToLongest = sorted(arrayOfRidesDurationAvgs, key=sorter)


# Second Longest AVG wait for Rides, ID number
secondLeastPopularRideID = arrayOfRidesDurationAvgs[-2][0]
SecondLeastPopularAttractionArray = []
for row in cur.execute("SELECT Name FROM attraction WHERE AttractionID=" + str(secondLeastPopularRideID)):
   SecondLeastPopularAttractionArray.append(row)

SecondLeastPopularAttraction = SecondLeastPopularAttractionArray[0][0]
print(SecondLeastPopularAttraction)
# Question 3 Least visited Resturant

sorter = (lambda x : (x[1]))
sortedAttractionsAndNumberOfCheckinsAtFood = sorted(attractionsAndNumberOfCheckinsAtFood, key=sorter)

print(attractionsAndNumberOfCheckinsAtFood)

# Be sure to close the connection
con.close()
                    