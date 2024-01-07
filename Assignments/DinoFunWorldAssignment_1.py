import pandas as pd
import sqlite3

dbfile = r"C:\Users\Austi\Git\DataVisualizationCSE578\Assignments\dinofunworld.db"


# 3 Questions to Awnser:
# What is the most popular aatraction to vist in the park?
# what ride (not that not all attractions are rides) has the second longest average visit time?
# Which Fast Food offering has the fewest vistiors?



# Common SQL commands I might need again: 
# SELECT column1, column2, ... FROM table_name;
# DISTINCT to get unquie values.

# Notes to self: 
# About question 1, How do we define popular? ( most checkins?)
# About question 2, remove all data with type as Shopping, Fast Food, Theater, and Beer Garden from table "Attraction". They are not rides!
# About question 3, remove all data with type that is not Fast Food.    

# Create a SQL connection to our SQLite database    
con = sqlite3.connect(dbfile)

cur = con.cursor()

#grab all Attractions 
allTypesOfAttractions= []
for row in cur.execute("SELECT DISTINCT type FROM attraction"):
    allTypesOfAttractions.append(row)

#grab all Attractions that are rides
allRides= []
for row in cur.execute("SELECT AttractionID FROM attraction WHERE Category LIKE '%Ride%' "):
    allRides.append(row)

for row in cur.execute("SELECT AttractionID FROM attraction WHERE Category LIKE '%Ride%' "):



# Be sure to close the connection
con.close()
                    