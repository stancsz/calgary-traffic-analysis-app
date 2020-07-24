import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from database import db
from database.db import ingest_data


def most_frequent(list):
    """
    # Function creates a histogram of values of: (Incident Info : count)
    # Will return description of incident info as well as frequency of occurence.
    # Sorted in Descending order so first element is the maximum number of occurences of Incidents.
    
    :param list: dataframe of file for incidents in a specific year 
    :return: hist[0]: Returns maximum value of incident in specific year
    """
    hist = pd.value_counts(list.incident_info, sort=True, ascending=False)
    return hist[0]


def compute_plot_data(df1, df2):
    '''
    Identify/plot maximum traffic volumes in Calgary between 2016-2018 (2019/20 data was not available)
    Identify/plot maximum accident volumes at specific intersection (using Column: Incident_Info) in Calgary between 2016-2020
    :param: df1: first dataframe for volume
    :param: df2: second dataframe for incident

    :return: volumes_x: Year for volumes (2016-2018)
    :return: volumes: Maximum volumes corresponding to specific years 2016-2018
    :return: incidents_x:Year for incidents (2016-2020)
    :return: incidents: Maximum incidents corresponding to specific years 2016-2020
    '''

    # Read csv files and load them into dataframe
    # df = db.ingest_data('/Users/sarangkumar/Desktop/Software/ENSF 592/Project_ENSF592/csv')

    # Initialize lists of year, volumes, incidents/accidents
    year = [2016, 2017, 2018, 2019, 2020]
    volumes = [0, 0, 0]
    incidents = [0, 0, 0, 0, 0]

    # Get and store dataframe for a specific year and type (volume or incident)
    vol_16 = db.get_dataframe_from_db_by_year('volume', 2016)
    vol_17 = db.get_dataframe_from_db_by_year('volume', 2017)
    vol_18 = db.get_dataframe_from_db_by_year('volume', 2018)

    # More data available (2019/20 years) for incidents
    inc_16 = db.get_dataframe_from_db_by_year('incident', 2016)
    inc_17 = db.get_dataframe_from_db_by_year('incident', 2017)
    inc_18 = db.get_dataframe_from_db_by_year('incident', 2018)
    inc_19 = db.get_dataframe_from_db_by_year('incident', 2019)
    inc_20 = db.get_dataframe_from_db_by_year('incident', 2020)

    # Sum values within 'volume' column to determine sum total
    volumes[0] = vol_16['volume'].max()
    volumes[1] = vol_17['volume'].max()
    volumes[2] = vol_18['volume'].max()

    # Initialize vol_condensed to store value of volumes dividied by a 1x10^5. Allows easier presentation
    vol_condensed = []
    for x in volumes:
        vol_condensed.append(x / 100000)


    # Sum values within 'count' column to determine sum total.
    # Note: All count values were equal to 1 and representing each separate incident
    incidents[0] = most_frequent(inc_16)
    incidents[1] = most_frequent(inc_17)
    incidents[2] = most_frequent(inc_18)
    incidents[3] = most_frequent(inc_19)
    incidents[4] = most_frequent(inc_20)
    volumes_x = year[:3]
    incidents_x = year
    return volumes_x, volumes, incidents_x, incidents

    # ####PLOT VOLUME GRAPH####
    #
    # # Plot scatter and line plot. Plotting volumes[0:3] because volumes available for 2016,17,18 only.
    # plt.scatter(year[0:3], vol_condensed)
    # plt.plot(year[0:3], vol_condensed, linestyle='-', color='green')
    #
    # # Plot Attributes
    # plt.title('Maximum Traffic Volume as a Function of Year')
    # plt.xlabel('Year')
    # plt.ylabel('Maximum Traffic Volume \n (x10^5)')
    #
    # # Increment year by 1 on x axis. Ie. prevents decimal point years on x-axis
    # plt.xticks(np.arange(min(year[0:3]), max(year[0:3]) + 1, 1.0))
    #
    # # Save figure and show plot
    # plt.savefig("Volume_Year.png")
    # plt.show()
    #
    # ####PLOT INCIDENTS GRAPH####
    # ##Graph plots maximum incident occurences (by Incident Info description column) in a specific year
    # # Plot scatter and line plot
    # plt.scatter(year, incidents)
    # plt.plot(year, incidents, linestyle='-', color='green')
    #
    # # Plot Attributes
    # plt.title('Maximum Traffic Accidents as a Function of Year')
    # plt.xlabel('Year')
    # plt.ylabel('Maximum Traffic Accidents')
    #
    # # Arrange axis with appropriate increments
    # plt.xticks(np.arange(min(year), max(year) + 1, 1.0))
    # plt.yticks(np.arange(0, max(incidents) + 5, 5))
    #
    # # Save figure and show plot
    # plt.savefig("Accident_Year.png")
    # plt.show()


def test():
    '''
    Function used to test file and debug 
    '''
    # year = [2016, 2017, 2018, 2019, 2020]
    # vol_list=[]
    # for i, val in enumerate(year):
    #     vol_list.append(val)
    # print(vol_list)

    csv_path = '../csv'
    df1, df2 = ingest_data(csv_path)  # ingest all csv data into mongo database
    for i in compute_plot_data(df1, df2):
        print(i)
    x1, y1, x2, y2 = compute_plot_data(df1, df2)

    return


if __name__ == '__main__':
    test()
