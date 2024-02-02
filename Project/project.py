import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from statsmodels.graphics.mosaicplot import mosaic


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

#Remove NULL JOB
del dictOfUniqueOccupation['NULL']

#colors to use in graphs
arrayOfColors = ['yellow','crimson','deepskyblue','green','aquamarine','violet','brown','lightsalmon','steelblue','cyan','olive','mediumseagreen','grey','orange']
color1 = "cornflowerblue"
color2 = "orange"

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

#----------------------------------------------------------------------------------------------------\
def bar_graph_of_occupations_by_income_groups():

    # What Jobs should we target when looking for ppl to recuirt to our school? 

    #make the bar graph        
    plt.bar(x=dictOfUniqueOccupation.keys(),height=dictOfUniqueOccupationUnder50k.values(), color = color1, label = "occupation under 50k", labels = "Yes")
    plt.bar(x=dictOfUniqueOccupation.keys(),height=dictOfUniqueOccupationOver50k.values(), color = color2, label = "occupation over 50k", labels = "Yes")

    plt.title('Total people per occupuation based on income groups')
    plt.xticks(rotation =45, ha = "right")
    plt.ylabel('Number of people')
    plt.xlabel('Occupation')
    plt.legend(('Income at or less then $50k','Income over $50k'),loc = 'upper right', )
    plt.show()

def donut_graphs_of_occupantions_by_income_groups():
    
    
    # del dictOfUniqueOccupation['Armed-Forces']
    # del dictOfUniqueOccupationUnder50k['Armed-Forces']  
    arrayOfPplPerOccupationUnder50k = dictOfUniqueOccupationUnder50k.values()

    plt.pie(arrayOfPplPerOccupationUnder50k,shadow=False,autopct='%1.2f%%',textprops={'fontsize':13}, colors=arrayOfColors, labels=dictOfUniqueOccupation.keys(), labeldistance =1.01 )		
    plt.title("Title")
    plt.axis("equal")
    plt.gcf().gca().add_artist(plt.Circle( (0,0), 0.7, color='white'))
    plt.show() 

    # del dictOfUniqueOccupationOver50k['Armed-Forces']
    arrayOfPplPerOccupationOver50k = dictOfUniqueOccupationOver50k.values()

    plt.pie(arrayOfPplPerOccupationOver50k,shadow=False,autopct='%1.2f%%',textprops={'fontsize':13}, colors=arrayOfColors, labels=dictOfUniqueOccupation.keys(), labeldistance =1.01 )		
    plt.title("Title")
    plt.axis("equal")
    plt.gcf().gca().add_artist(plt.Circle( (0,0), 0.7, color='white'))
    plt.show()


def Scatter_plot_age_vs_college():
    # User Story 3 - People that didnt finish college, over all ages


    #remove any one that didnt finish college
    indexeducation = adultsStats[(dictOfAgeAndSchoolAndIncome['education'] == 'Bachelors') | (dictOfAgeAndSchoolAndIncome['education'] == 'Prof-school')| (dictOfAgeAndSchoolAndIncome['education'] == 'Assoc-acdm')| (dictOfAgeAndSchoolAndIncome['education'] == 'Assoc-voc')| (dictOfAgeAndSchoolAndIncome['education'] == 'Doctorate')| (dictOfAgeAndSchoolAndIncome['education'] == 'Masters')].index
    dictOfAgeAndSchoolAndIncome.drop(indexeducation, inplace=True)

    dfAgeAndSchoolAndIncome = adultsStats[['age','hours-per-week','income']]

    ageOfPeopleUnder50k = []
    hoursOfPeopleUnder50k = []
    ageOfPeopleOver50k = []
    hoursOfPeopleOver50k = []
    for row in dictOfAgeAndSchoolAndIncome.iterrows():

        age = row[1][0]
        hours = row[1][1]
        income = row[1][2]
        
        if(age == 'NULL' or hours == 'NULL' or income == 'NULL'):
            continue
        elif(income == '<=50K'):
            ageOfPeopleUnder50k.append(age)
            hoursOfPeopleUnder50k.append(hours)
        elif(income == '>50K'):
            ageOfPeopleOver50k.append(age)
            hoursOfPeopleOver50k.append(hours)
        else:
            print("Something is wrong check for this income:" + str(income))
    x1 = ageOfPeopleUnder50k
    y1 = hoursOfPeopleUnder50k 
    x2 = ageOfPeopleOver50k 
    y2 = hoursOfPeopleOver50k

    plt.scatter(x1,y1)
    plt.scatter(x2,y2)
    plt.show()

def mosaic_plot_location_by_gender():
     

     
    df = adultsStats[['native-counntry','sex','income']]

    dict = {('Inside Of USA', 'Female', 'Income > 50k') : 0,
            ('Inside Of USA', 'Male', 'Income > 50k') : 0, 
            ('Outside Of USA', 'Female', 'Income > 50k') : 0, 
            ('Outside Of USA', 'Male', 'Income > 50k') : 0,
            ('Inside Of USA', 'Female', 'Income <= 50k') : 0,
            ('Inside Of USA', 'Male', 'Income <= 50k') : 0, 
            ('Outside Of USA', 'Female', 'Income <= 50k') : 0, 
            ('Outside Of USA', 'Male', 'Income <= 50k') : 0  }
    

    for row in df.iterrows():
        country = row[1][0]
        sex = row[1][1]
        income = row[1][2]
        if(country == 'NULL' or sex == 'NULL' or income == 'NULL'):
            continue
        elif(country=='United-States' or country=='Puerto-Rico' or country=='Outlying-US(Guam-USVI-etc)'):
            if(sex == 0):
                if(income == '<=50K'):
                    dict[('Inside Of USA', 'Female', 'Income <= 50k')] = dict[('Inside Of USA', 'Female', 'Income <= 50k')] + 1
                if(income == '>50K'):
                    dict[('Inside Of USA', 'Female', 'Income > 50k')] = dict[('Inside Of USA', 'Female', 'Income > 50k')] + 1
                
            elif(sex == 1):
                if(income == '<=50K'):
                    dict[('Inside Of USA', 'Male', 'Income <= 50k')] = dict[('Inside Of USA', 'Male', 'Income <= 50k')] + 1
                if(income == '>50K'):
                    dict[('Inside Of USA', 'Male', 'Income > 50k')] = dict[('Inside Of USA', 'Male', 'Income > 50k')] + 1
            else:
                print("THERE MIGHT BE A PROBLEM WITH THIS: " + row)
        else:
            if(sex == 0):
                if(income == '<=50K'):
                    dict[('Outside Of USA', 'Female', 'Income <= 50k')] = dict[('Outside Of USA', 'Female', 'Income <= 50k')] + 1
                if(income == '>50K'):
                    dict[('Outside Of USA', 'Female', 'Income > 50k')] = dict[('Outside Of USA', 'Female', 'Income > 50k')] + 1
                
            elif(sex == 1):
                if(income == '<=50K'):
                    dict[('Outside Of USA', 'Male', 'Income <= 50k')] = dict[('Outside Of USA', 'Male', 'Income <= 50k')] + 1
                if(income == '>50K'):
                    dict[('Outside Of USA', 'Male', 'Income > 50k')] = dict[('Outside Of USA', 'Male', 'Income > 50k')] + 1
            else:
                print("THERE MIGHT BE A PROBLEM WITH THIS: " + row)
                
    print(dict)
    #https://www.statsmodels.org/devel/generated/statsmodels.graphics.mosaicplot.mosaic.html
    # dictOfColor = {('Inside Of USA', 'Female', 'above50k') : 'b',
    #         ('Inside Of USA', 'Male', 'above50k') : 'g', 
    #         ('Outside Of USA', 'Female', 'above50k') : 0, 
    #         ('Outside Of USA', 'Male', 'above50k') : 0,
    #         ('Inside Of USA', 'Female', 'below50k') : 0,
    #         ('Inside Of USA', 'Male', 'below50k') : 0, 
    #         ('Outside Of USA', 'Female', 'below50k') : 0, 
    #         ('Outside Of USA', 'Male', 'below50k') : 0  }
    label=lambda k:{k:str(round(dict[k]/sum(dict.values())*100,1))+'%'}[k]
    mosaic(dict, gap=0.003,properties={},labelizer=label)
    plt.title("Birthright US Citizens and Gender compared by Income Groups")
    plt.show()
        



# bar_graph_of_occupations_by_income_groups()
# donut_graphs_of_occupantions_by_income_groups()
# Scatter_plot_age_vs_college()
mosaic_plot_location_by_gender()


# print(uniqueOccupation)
#print(adultsStats[adultsStats['workclass'] == '?']) FINDS SPECFIC VAL in COL
#print(adultsStats['occupation'].unique())  FINDS UNQUIE VALS IN COL
