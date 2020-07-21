import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from database import db

'''
Identify/plot total traffic volumes in Calgary between 2016-2018 (2019/20 data was not available)
Identify/plot total accident volumes in Calgary between 2016-2020 
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
volumes[0] = vol_16['volume'].sum()
volumes[1] = vol_17['volume'].sum()
volumes[2] = vol_18['volume'].sum()

#Initialize vol_mill to store value of volumes dividied by a million. Allows easier presentation
vol_million = []
for x in volumes:
    vol_million.append(x/1000000)


#Sum values within 'count' column to determine sum total. 
#Note: All count values were equal to 1 and representing each separate incident
incidents[0] = inc_16['count'].sum()
incidents[1] = inc_17['count'].sum()
incidents[2] = inc_18['count'].sum()
incidents[3] = inc_19['count'].sum()
incidents[4] = inc_20['count'].sum()



####PLOT VOLUME GRAPH####

#Plot scatter and line plot. Plotting volumes[0:3] because volumes available for 2016,17,18 only. 
plt.scatter(year[0:3], vol_million)
plt.plot(year[0:3],vol_million,linestyle = '-',color='green')

#Plot Attributes
plt.title('Total Traffic Volume as a Function of Year')
plt.xlabel('Year')
plt.ylabel('Total Traffic Volume \n (Millions)')


#Increment year by 1 on x axis. Ie. prevents decimal point years on x-axis
plt.xticks(np.arange(min(year[0:3]), max(year[0:3])+1, 1.0))

#Save figure and show plot
plt.savefig("Volume_Year.jpg")
plt.show()


####PLOT INCIDENTS GRAPH####

#Plot scatter and line plot
plt.scatter(year, incidents)
plt.plot(year,incidents,linestyle = '-',color='green')

#Plot Attributes
plt.title('Total Traffic Accidents as a Function of Year')
plt.xlabel('Year')
plt.ylabel('Total Traffic Accidents')

#Arrange axis with appropriate increments
plt.xticks(np.arange(min(year), max(year)+1, 1.0))
plt.yticks(np.arange(0, max(incidents)+1000, 1000))

#Save figure and show plot
plt.savefig("Accident_Year.jpg")
plt.show()


####DATAFRAME CONTAINING VOLUME WITH CORRESPONDING YEAR####
Vol_data = {'Year': year[0:3],'Total Traffic Volume': volumes}
Vol_df = pd.DataFrame(Vol_data,columns=['Year','Total Traffic Volume'])
print(Vol_df)

####DATAFRAME CONTAINING INCIDENTS WITH CORRESPONDING YEAR####
Inc_data = {'Year': year,'Total Traffic Incidents': incidents}
Inc_df = pd.DataFrame(Inc_data,columns=['Year','Total Traffic Incidents'])
print(Inc_df)


