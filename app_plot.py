import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from database import db

'''
Identify/plot maximum traffic volumes in Calgary between 2016-2018 (2019/20 data was not available)
Identify/plot maximum accident volumes at specific intersection (using Column: Incident_Info) in Calgary between 2016-2020 
'''

# Read csv files and load them into dataframe
df = db.ingest_data('/Users/sarangkumar/Desktop/Software/ENSF 592/Project_ENSF592/csv')

#Initialize lists of year, volumes, incidents/accidents
year = [2016,2017,2018,2019,2020]
volumes =[0,0,0]
incidents =[0,0,0,0,0]

#Get and store dataframe for a specific year and type (volume or incident)
vol_16 = db.get_dataframe_from_db_by_year(df, 2016, 'traffic_volume')
vol_17 = db.get_dataframe_from_db_by_year(df, 2017, 'traffic_volume')
vol_18 = db.get_dataframe_from_db_by_year(df, 2018, 'traffic_volume')

#More data available (2019/20 years) for incidents
inc_16 = db.get_dataframe_from_db_by_year(df, 2016, 'traffic_incident')
inc_17 = db.get_dataframe_from_db_by_year(df, 2017, 'traffic_incident')
inc_18 = db.get_dataframe_from_db_by_year(df, 2018, 'traffic_incident')
inc_19 = db.get_dataframe_from_db_by_year(df, 2019, 'traffic_incident')
inc_20 = db.get_dataframe_from_db_by_year(df, 2020, 'traffic_incident')

#Sum values within 'volume' column to determine sum total
volumes[0] = vol_16['volume'].max()
volumes[1] = vol_17['volume'].max()
volumes[2] = vol_18['volume'].max()


#Initialize vol_condensed to store value of volumes dividied by a 1x10^5. Allows easier presentation
vol_condensed = []
for x in volumes:
    vol_condensed.append(x/100000)

#Function creates a histogram of values of: (Incident Info : count)
#Will return description of incident info as well as frequency of occurence. 
#Sorted in Descending order so first element is the maximum number of occurences of Incidents.
def most_frequent(list):
    hist = pd.value_counts(list.incident_info, sort = True, ascending =False)
    return hist[0]

#Sum values within 'count' column to determine sum total. 
#Note: All count values were equal to 1 and representing each separate incident
incidents[0] = most_frequent(inc_16)
incidents[1] = most_frequent(inc_17)
incidents[2] = most_frequent(inc_18)
incidents[3] = most_frequent(inc_19)
incidents[4] = most_frequent(inc_20)


####PLOT VOLUME GRAPH####

#Plot scatter and line plot. Plotting volumes[0:3] because volumes available for 2016,17,18 only. 
plt.scatter(year[0:3], vol_condensed)
plt.plot(year[0:3],vol_condensed,linestyle = '-',color='green')

#Plot Attributes
plt.title('Maximum Traffic Volume as a Function of Year')
plt.xlabel('Year')
plt.ylabel('Maximum Traffic Volume \n (x10^5)')

#Increment year by 1 on x axis. Ie. prevents decimal point years on x-axis
plt.xticks(np.arange(min(year[0:3]), max(year[0:3])+1, 1.0))

#Save figure and show plot
plt.savefig("Volume_Year.png")
plt.show()


####PLOT INCIDENTS GRAPH####
##Graph plots maximum incident occurences (by Incident Info description column) in a specific year
#Plot scatter and line plot
plt.scatter(year, incidents)
plt.plot(year,incidents,linestyle = '-',color='green')

#Plot Attributes
plt.title('Maximum Traffic Accidents as a Function of Year')
plt.xlabel('Year')
plt.ylabel('Maximum Traffic Accidents')

#Arrange axis with appropriate increments
plt.xticks(np.arange(min(year), max(year)+1, 1.0))
plt.yticks(np.arange(0, max(incidents)+5, 5))

#Save figure and show plot
plt.savefig("Accident_Year.png")
plt.show()



