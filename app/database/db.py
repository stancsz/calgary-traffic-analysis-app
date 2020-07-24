"""
this module is the infrastructure for the db interactions. calls and create a local db
to provide basic infrastructure for the main program
https://docs.mongodb.com/drivers/pymongo
please make sure mongod is active before running this module
"""
import os
import datetime
from pathlib import Path
from pprint import pprint
import pandas as pd
import pymongo
import json


def ingest_dataframe_to_db(df, db_name, collection_name, db_url='localhost', db_port=27017):
    """
    Imports a pandas dataframe into a mongo colection.

    :param df: pandas dataframe
    :param db_name: name of the database (mongodb)
    :param collection_name: name of the collection
    :param db_url: url of the database
    :param db_port: port number of the database
    :return: None
    """
    mongo_client = pymongo.MongoClient(db_url, db_port)
    db_connection = mongo_client[db_name]
    db_collection = db_connection[collection_name]
    payload = json.loads(df.to_json(orient='records'))

    db_collection.delete_many({})
    db_collection.insert_many(payload)
    print('Collection: ', '\'' + collection_name + '\'', ' is imported in DB:', '\'' + db_name + '\'')


def get_dataframe_from_mongo(db_name, collection_name, db_url='localhost', db_port=27017):
    """
    Gets a dataframe from the specified collection inside the specified database.

    :param db_name: name of the database (mongodb)
    :param collection_name: name of the collection
    :param db_url: url of the database
    :param db_port: port number of the database
    :return: pandas dataframe
    """
    check_collection_in_dbs(collection_name)
    mongo_client = pymongo.MongoClient(db_url, db_port)
    db_connection = mongo_client[db_name]
    db_collection = db_connection[collection_name]
    query = {}
    cursor = db_collection.find(query)
    data_frame = pd.DataFrame(list(cursor))
    del data_frame['_id']
    return data_frame


def ingest_data(csv_key):
    """
    Reads all the csv files from the csv_key as path (works as absolute path on win environments)
    Separates csv files if having 'Flow' or 'Incidents' keywords in them, then calls the 
    import_csv_into_dataframe() accordingly.

    Concatenates result of each csv processing into one unified pandas dataframe (all_incidents or all_volumes)
    When all csv files are processed, it imports all dataframes into database.

    :param csv_key: path for the csv_files (absolute for Win env)
    :return: None
    """

    # csv_key = 'csv'

    all_incidents = pd.DataFrame()
    all_volumes = pd.DataFrame()

    for csv_file in os.listdir(csv_key):
        is_csv = (csv_file.endswith(".csv"))
        is_incident = (csv_file.find('Incidents') != -1)
        is_volume = (csv_file.find('Flow') != -1) or (csv_file.find('Volume') != -1)
        path = os.path.join(csv_key, csv_file)
        if is_csv and is_incident:
            df = import_csv_into_dataframe(path, type='traffic_incident')
            # ignore index is to re-index all entries when merging (so that 2nd collection entries do not start from 0)
            all_incidents = pd.concat([all_incidents, df], ignore_index=True)
        elif is_csv and is_volume:
            df = import_csv_into_dataframe(path, type='traffic_volume')
            # ignore index is to re-index all entries when merging (so that 2nd collection entries do not start from 0)
            all_volumes = pd.concat([all_volumes, df], ignore_index=True)
        else:
            continue

    # clean duplicate entries
    all_incidents = all_incidents[~all_incidents.duplicated()]
    all_volumes = all_volumes[~all_volumes.duplicated()]

    # return all_incidents
    # import unified dataframes into db
    ingest_dataframe_to_db(all_volumes, 'db_volume', 'all_volumes')
    ingest_dataframe_to_db(all_incidents, 'db_incident', 'all_incidents')
    return all_volumes, all_incidents


def reload_ingestion():
    """
    this function is to reload ingestion, by first calling drop all db
    and then re-ingest all data.
    :return:
    """
    drop_all_db()
    ingest_data()


def check_collection_in_dbs(collection_name, db_url='localhost', db_port=27017):
    """
    Reloads all dbs if program encountered a missing collection,
    if missing a collection, reload the entire data ingestion.

    :param collection_name: name of the collection
    :param db_url: url of the database
    :param db_port: port number of the database
    :return: None
    """
    mongo_client = pymongo.MongoClient(db_url, db_port)
    in_incident = (collection_name in mongo_client['db_incident'].list_collection_names())
    in_volume = (collection_name in mongo_client['db_volume'].list_collection_names())
    if not in_incident and not in_volume:
        drop_all_db()
        ingest_data()
        print('Collection not found, reloading ingestion.')


def print_collection(db_name, collection_name, db_url, db_port):
    """
    Prints the first 10 items in the collection found on specified mongodb/db_name/collection_name

    :param db_name: name of the database
    :param collection_name: name of the collection
    :param db_url: url of the database
    :param db_port: port number of the database
    :return: None
    """
    mongo_client = pymongo.MongoClient(db_url, db_port)
    db_connection = mongo_client[db_name]
    db_collection = db_connection[collection_name]
    cursor = db_collection.find({}).limit(10)
    print('printing first 10 items')
    for doc in cursor:
        pprint(doc)


def drop_collection(db_name, collection_name, db_url='localhost', db_port=27017):
    """
    Check collection in a db_name, and then drops it if it already exists.
    Prints a message to the CLI regarding the outcome.

    :param db_name: name of the database
    :param collection_name: name of the collection
    :param db_url: url of the database
    :param db_port: port number of the database
    :return: None
    """
    mongo_client = pymongo.MongoClient(db_url, db_port)
    db_connection = mongo_client[db_name]
    db_collection = db_connection[collection_name]
    print(db_connection.list_collection_names())
    if collection_name in db_connection.list_collection_names():
        print(collection_name, 'exists:', True)
        db_collection.drop()
        print(collection_name, 'dropped')
    else:
        print(collection_name, 'exists:', False)


def create_db(db_name, db_url='localhost', db_port=27017):
    """
    creates an empty database
    :param db_name: db to drop connection
    :param collection_name: collection to drop
    :param db_url: db's url
    :param db_port: port for the db
    :return:
    """
    mongo_client = pymongo.MongoClient(db_url, db_port)
    db_connection = mongo_client[db_name]
    


def drop_all_db(db_url='localhost', db_port=27017):
    """
    Drops all databases which contain keyword 'db_' (in our application they are user defined databases).
    Prints a message to the console when a database is successfully dropped. 

    :param db_url: url of the database
    :param db_port: port number of the database
    :return: None
    """

    mongo_client = pymongo.MongoClient(db_url, db_port)
    db_list = mongo_client.list_database_names()
    for i in db_list:
        is_user_db = (i.find('db_') != -1)
        if is_user_db:
            mongo_client.drop_database(i)
            print('user database', i, 'is dropped')


def import_csv_into_dataframe(path, type):
    """
    Reads target csv file and puts that into a dataframe in a standard way, according to the type specified.

    For traffic_volume, column structure will be
        -- 'segment_name', 'year', 'the_geom', 'length_m', 'volume' --
    For traffic_incident, column structure will be
        -- 'incident_info', 'description', 'start_dt', 'modified_dt', 'year',
        'quadrant', 'longitude', 'latitude', 'location', 'count' ', 'grid_num' --

    :param path: path to the target csv file to be read.
    :param type: type of csv to be read, either 'traffic_volume' or 'traffic_incident'
    :return: re-structured dataframe
    """
    dataFrame = pd.read_csv(path)

    print('Importing ' + path + ' into dataframe.')

    # make all column headers lower case
    for col in dataFrame.columns:
        dataFrame.rename(columns={col: col.lower()}, inplace=True)

    ## Traffic Flow Dataframe
    if type == 'traffic_volume':

        # standardize column header names
        if 'secname' in dataFrame.columns:
            dataFrame.rename(columns={'secname': 'segment_name'}, inplace=True)
        if 'shape_leng' in dataFrame.columns:
            dataFrame.rename(columns={'shape_leng': 'length_m'}, inplace=True)
        if 'multilinestring' in dataFrame.columns:
            dataFrame.rename(columns={'multilinestring': 'the_geom'}, inplace=True)
        if 'year_vol' in dataFrame.columns:
            dataFrame.rename(columns={'year_vol': 'year'}, inplace=True)

        # re-ordering dataframe columns
        return dataFrame.reindex(columns=['segment_name', 'year', 'the_geom', 'length_m', 'volume'])

    elif type == 'traffic_incident':

        # standardize column header names and get rid of unused headers
        if 'id' in dataFrame.columns:
            del dataFrame['id']

        if 'incident info' in dataFrame.columns:
            dataFrame.rename(columns={'incident info': 'incident_info'}, inplace=True)

        # build year column by parsing start_dt column
        years = []
        for dtStr in dataFrame.start_dt:
            years.append(datetime.datetime.strptime(dtStr, '%m/%d/%Y %I:%M:%S %p').year)
        dataFrame['year'] = years

        # calculate gps grids of the incident and add them to the dataframe
        grids = []
        for index, row in dataFrame.iterrows():
            grids.append(calculate_geogrid_number(row['latitude'], row['longitude'], 6)) #use 6x6 grids
        dataFrame['grid_num'] = grids

        # re-ordering dataframe columns
        return dataFrame.reindex(
            columns=['incident_info', 'description', 'start_dt', 'modified_dt', 'year', 'quadrant', 'latitude',
                     'longitude', 'location', 'count', 'grid_num'])


def calculate_geogrid_number(latitude, longitude, grid_size):
    """
    Divides Calgary into equi-distant square geographical grids, using the grid_size argument.
    If grid_size is 10, then Calgary will be divided into 10x10 = 100 grids.
    Then, calculates the geogrid number for the given latitude, longitude pair.
    Please refer to \static\grid.png to a visual representation of a 6x6 sample grid layout.
    example, if gridsize = 10 then
    10 x 10 grid:
    Grid 0 = grid on the very south-west
    Grid 9 = grid on the very south-east

    Grids 44, 45, 54, 55 = grids close to the city center

    Grid 90 = grid on the very north-west
    Grid 99 = grid on the very north-east

    :param latitude: latitude of the gps point, should be supplied in decimal format (ie, 40.103)
    :param longitude: longitude of the gps point, should be supplied in decimal format (ie, 40.103)
    :return: geo-grid number of the given latitude, longitude pair. -1 if point is calculated outside Calgary.
    """

    # GPS boundaries for Calgary
    longitude_max = -113.75
    longitude_min = -114.35
    latitude_max = 51.25
    latitude_min = 50.75

    # calculate bounds for each grid, calculate equi-distant x-y grids
    grid_long = list(range(1, grid_size + 1))
    grid_lati = list(range(1, grid_size + 1))

    grid_long = [((longitude_max - longitude_min) / grid_size) * i + longitude_min for i in grid_long]
    grid_lati = [((latitude_max - latitude_min) / grid_size) * i + latitude_min for i in grid_lati]

    # compare inputted long and lati to the look-up tables (grid_long and grid_lati)
    # increase in latitude (corresponds going further north)
    for i in range(grid_size):
        if latitude < latitude_min or latitude > latitude_max:
            pointYGrid = -1 # point is outside Calgary geo bounds, assign -1 for those entries
            break
        elif latitude <= grid_lati[i]:
            pointYGrid = i
            break

    # increase in longitude (corresponds going further east)
    for i in range(grid_size):
        if longitude < longitude_min or longitude > longitude_max:
            pointXGrid = -1 # point is outside Calgary geo bounds, assign -1 for those entries
            break
        if longitude <= grid_long[i]:
            pointXGrid = i
            break

    if pointYGrid == -1 or pointXGrid == -1:
        gridNumber = -1
    else:
        gridNumber = (pointYGrid * grid_size) + pointXGrid

    return gridNumber


def get_dataframe_from_db_by_year(db_type, year):
    """
    returns a dataframe from mongodb by its given type and filtered by year
    :param db_type: type of database to read from, either 'volume' or 'incident'
    :param year: year value to apply on the dataframe to filter entries.
    :return: dataframe (filtered by year)
    """
    if db_type == 'volume':
        df = get_dataframe_from_mongo('db_volume','all_volumes')
    elif db_type == 'incident':
        df = get_dataframe_from_mongo('db_incident','all_incidents')
        
    return_df = df[df['year'] == year]
    return return_df

def sort_dataframe_by(df_in, type):
    """
    Sorts a given dataframe by its given type.
    (if type is volume then sorts by 'volume', if type is incident then sorts by count)
    
    :param df_in: dataframe to be sorted
    :param type: type of dataframe, either 'volume' or 'incident'
    :return: a copy of the inputted dataframe which is sorted.
    """
    if type == 'volume':
        sortBy = 'volume'
        # Sort df
        df = df_in
        df.sort_values(by=sortBy, inplace=True, ascending=False)
        return df

    elif type == 'incident':
        #incident sorting is done through gridding first and summing values for each grid
        return sort_incidents_into_grids(df_in)


def sort_incidents_into_grids(df):
    """
    Takes a dataframe of type incidents and then makes another dataframe which puts all entries
    sharing the same grid number and also calculation total count of incidents per grid number.
    
    :param df: incidents dataframe to be processed into grids.
    :return: a new dataframe with columns grid_number and total incidents/grid.
    """
    newDf = pd.DataFrame(columns=['grid_num', 'incidents'])
    rowNum = 0
    #iterate on min grid number to max found in the incidents dataframe.
    for i in range(df['grid_num'].min(), df['grid_num'].max()):
        # filter entries to one grid at a time.
        df_OnlyOneGrid = df[df.grid_num == i]

        # populate grid number column for the new dataframe.
        grid_Num = i

        # populate total incidents column for the new dataframe.
        incidents = df_OnlyOneGrid['count'].sum()

        # make a new row from the calculated values above.
        newDf.loc[rowNum] = [grid_Num, incidents]

        #go to the next row.
        rowNum += 1

    # return the newly build grid_num - total incidents dataframe.
    newDf.sort_values(by='incidents', inplace=True, ascending=False)
    return newDf


def test():
    """
    Testing sub-routine.
    :return: None
    """
    # Read csv files and load them onto db
    df1, df2 = ingest_data('../csv')
    for year in range(2016, 2019):

        df=get_dataframe_from_db_by_year('volume', year)
        print(df.columns)
        print(sort_dataframe_by(df,'volume'))



if __name__ == "__main__":
    test()
