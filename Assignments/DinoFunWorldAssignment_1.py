import pandas as pd
import sqlite3

dbfile = r"C:\Users\Austi\Git\DataVisualizationCSE578\Assignments\dinofunworld.db"

# Create a SQL connection to our SQLite database    
con = sqlite3.connect(dbfile)

cur = con.cursor()
print(dbfile)
# The result of a "cursor.execute" can be iterated over by row
for row in cur.execute("SELECT * FROM attraction"):
    print(row)

# Be sure to close the connection
con.close()
                    