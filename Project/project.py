import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


csvfile = r"Project\adult.csv"

#data frame with all the data.
adultsStats = pd.read_csv(csvfile,header=0)

#remove fnlwgt because it is not being used for this project.
adultsStats = adultsStats.drop(['fnlwgt'],axis=1)

#Look for '?' and replace with nulls
adultsStats =   adultsStats.replace('?','NULL')

#Transform Sex data to binary form
adultsStats['sex'] = adultsStats['sex'].replace('Female',0)
adultsStats['sex'] = adultsStats['sex'].replace('Male',1)

dictOfUniqueOccupation = {}
#get a dictonary of all the occupations in the data frame
for val in adultsStats['occupation'].unique():
    dictOfUniqueOccupation[val] = 0

#----------------------------------------------------------------------------------------------------\
def bar_graph_of_occupations_by_income_groups():

    # What Jobs should we target when looking for ppl to recuirt to our school? 
 

    #Remove NULL JOB
    del dictOfUniqueOccupation['NULL']
    #create 2 dict one for tracking ppl abve 50k one for below.
    dictOfUniqueOccupationUnder50k = dict(dictOfUniqueOccupation)
    dictOfUniqueOccupationOver50k = dict(dictOfUniqueOccupation)

    for row in adultsStats.iterrows():
        occupation = row[1][5]
        income = row[1][13]
        sex = row[1][8]
        # Ignore Jobs with NULL not in the dict
        if(occupation == 'NULL'):
            continue
        if(income == '<=50K'):
            dictOfUniqueOccupationUnder50k[occupation] = dictOfUniqueOccupationUnder50k[occupation] + 1
        elif(income == '>50K'):
            dictOfUniqueOccupationOver50k[occupation] = dictOfUniqueOccupationOver50k[occupation] + 1
        else:
            print("Something is wrong check for this income:" + str(income))

    #make the bar graph        
    plt.bar(x=dictOfUniqueOccupation.keys(),height=dictOfUniqueOccupationUnder50k.values(), color = "cornflowerblue", label = "occupation under 50k", labels = "Yes")
    plt.bar(x=dictOfUniqueOccupation.keys(),height=dictOfUniqueOccupationOver50k.values(), color = "orange", label = "occupation over 50k", labels = "Yes")

    plt.title('Total people per occupuation based on income groups')
    plt.xticks(rotation =45, ha = "right")
    plt.ylabel('Number of people')
    plt.xlabel('Occupation')
    plt.legend(('Income at or less then $50k','Income over $50k'),loc = 'upper right', )
    plt.show()

def donut_graphs_of_occupantions_by_income_groups():
    print("hi")

bar_graph_of_occupations_by_income_groups()
    


# print(uniqueOccupation)
#print(adultsStats[adultsStats['workclass'] == '?']) FINDS SPECFIC VAL in COL
#print(adultsStats['occupation'].unique())  FINDS UNQUIE VALS IN COL
