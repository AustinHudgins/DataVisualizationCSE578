import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

dbfile = r"C:\Users\Austi\Git\DataVisualizationCSE578\Assignments\dinofunworld.db"




# Create a SQL connection to our SQLite database    
con = sqlite3.connect(dbfile)

cur = con.cursor()

visitorIDandsequencesDict = {}
for row in cur.execute("SELECT visitorID, sequence FROM sequences where visitorID IN (165316, 1835254, 296394, 404385, 448990)"):
    squence = row[1]
    splitsquence = squence.split("-")
    visitorIDandsequencesDict[row[0]] = splitsquence
#print(visitorIDandsequencesDict)

for()
# # Be sure to close the connection
con.close()
                   
