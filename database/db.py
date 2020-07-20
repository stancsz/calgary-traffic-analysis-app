"""
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


# def import_csv_to_mongo(csv_path, db_name, collection_name, db_url, db_port):
def import_csv_to_db(csv_path, db_name, collection_name, db_url='localhost', db_port=27017):
    """
    Imports a csv file at path csv_name to a mongo colection
    returns: count of the documants in the new collection

    :param csv_path:
    :param db_name:
    :param collection_name:
    :param db_url:
    :param db_port:
    :return:
    """
    mongo_client = pymongo.MongoClient(db_url, db_port)
    db_connection = mongo_client[db_name]
    db_collection = db_connection[collection_name]
    data = pd.read_csv(csv_path)

    payload = json.loads(data.to_json(orient='records'))
    db_collection.delete_many({})
    db_collection.insert_many(payload)
    print('Collection: ', '\'' + collection_name + '\'', ' is imported in DB:', '\'' + db_name + '\'')

def import_dataframe_to_db(df, db_name, collection_name, db_url='localhost', db_port=27017):
    """
    Imports a pandas dataframe into a mongo colection

    :param df:
    :param db_name:
    :param collection_name:
    :param db_url:
    :param db_port:
    :return:
    """
    mongo_client = pymongo.MongoClient(db_url, db_port)
    db_connection = mongo_client[db_name]
    db_collection = db_connection[collection_name]
    payload = json.loads(df.to_json(orient='records'))
    # print(payload)
    db_collection.delete_many({})
    db_collection.insert_many(payload)
    print('Collection: ', '\'' + collection_name + '\'', ' is imported in DB:', '\'' + db_name + '\'')


def get_dataframe_from_mongo(db_name, collection_name, db_url='localhost', db_port=27017):
    """
    Get a dataframe from a collection in a mongodb

    :param db_name:
    :param collection_name:
    :param db_url:
    :param db_port:
    :return:
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


def get_dataframe_from_mongo_dummy(csv_path):
    """
    will return a dataframe which will be the exactly the same as the real one
    read from mongodb
    :return: a dummy dataframe
    """
    # absolute_path = os.path.abspath(__file__)
    # current_path = os.path.dirname(absolute_path)
    # os.chdir(current_path)
    data = pd.read_csv(csv_path)
    return data


def ingest_data(csv_key):
    # csv_key = 'csv'
    all_incidents = pd.DataFrame()
    all_volumes = pd.DataFrame()

    for csv_file in os.listdir(csv_key):
        is_csv = (csv_file.endswith(".csv"))
        is_incident = (csv_file.find('Incidents') != -1)
        is_volume = (csv_file.find('Flow') != -1) or (csv_file.find('Volume') != -1)
        path = os.path.join(csv_key, csv_file)
        new_coll_name = Path(path).resolve().stem.lower()
        if is_csv and is_incident:
            df = import_csv_into_dataframe(path, type='traffic_incident')
            # ignore index is to re-index all entries when merging (so that 2nd collection entries do not start from 0)
            all_incidents = pd.concat([all_incidents, df], ignore_index=True)
            #import_csv_to_db(path, 'db_incident', new_coll_name)
        elif is_csv and is_volume:
            df = import_csv_into_dataframe(path, type='traffic_volume')
            # ignore index is to re-index all entries when merging (so that 2nd collection entries do not start from 0)
            all_volumes = pd.concat([all_volumes, df], ignore_index=True)
            #import_csv_to_db(path, 'db_volume', new_coll_name)
        else:
            continue

    # import unified dataframes into db
    import_dataframe_to_db(all_volumes, 'db_volume', 'all_volumes')
    import_dataframe_to_db(all_incidents, 'db_incident', 'all_incidents')

def reload_ingestion():
    drop_all_db()
    ingest_data()


def check_collection_in_dbs(collection_name, db_url='localhost', db_port=27017):
    """
    reloads all dbs if program encountered a missing collection,
    if missing a collection, reload the entire data ingestion.
    :return:
    """
    mongo_client = pymongo.MongoClient(db_url, db_port)
    in_incident = (collection_name in mongo_client['db_incident'].list_collection_names())
    in_volume = (collection_name in mongo_client['db_volume'].list_collection_names())
    if not in_incident and not in_volume:
        reload_ingestion()


def print_collection(db_name, collection_name, db_url, db_port):
    """
    :param db_name:
    :param collection_name:
    :param db_url:
    :param db_port:
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
    check collection in a db_connection, and then drop it if it exists

    :param db_name:
    :param collection_name:
    :param db_url:
    :param db_port:
    :return:
    """
    mongo_client = pymongo.MongoClient(db_url, db_port)
    db_connection = mongo_client[db_name]
    db_collection = db_connection[collection_name]
    print(db_connection.list_collection_names())
    # col_name = 'Programming Languages'
    if collection_name in db_connection.list_collection_names():
        print(collection_name, 'exists:', True)
        db_collection.drop()
        print(collection_name, 'dropped')
    else:
        print(collection_name, 'exists:', False)


def create_db(db_name, collection_name, db_url='localhost', db_port=27017):
    """
    creating an empty database
    :return:
    """
    mongo_client = pymongo.MongoClient(db_url, db_port)
    db_connection = mongo_client[db_name]


def drop_all_db(db_url='localhost', db_port=27017):
    mongo_client = pymongo.MongoClient(db_url, db_port)
    db_list = mongo_client.list_database_names()
    for i in db_list:
        is_user_db = (i.find('database') != -1)
        if is_user_db:
            mongo_client.drop_database(i)
            print('user database', i, 'is dropped')


def import_csv_into_dataframe(path, type):
    """
    Reads the path provided csv file and puts that into a dataframe in a standard way.
    For traffic_volume, column structure will be 'segment_name', 'year', 'the_geom', 'length_m', 'volume'
    For traffic_incident, column structure will be 'incident_info', 'description', 'start_dt', 'modified_dt', 'year', 'quadrant', 'longitude', 'latitude', 'location', 'count'

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
        return dataFrame.reindex(columns= ['segment_name', 'year', 'the_geom', 'length_m', 'volume'])

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

        # re-ordering dataframe columns
        return dataFrame.reindex(columns= ['incident_info', 'description', 'start_dt', 'modified_dt', 'year', 'quadrant', 'longitude', 'latitude', 'location', 'count'])


def get_dataframe_from_db_by_year(year, type):
    """
    returns a dataframe from mongodb by its given type and filters entries by year
    :return: dataframe (filtered by year)
    """
    if type == 'traffic_volume':
        databaseName = 'db_volume'
        collectionName = 'all_volumes'
        
    elif type == 'traffic_incident':
        databaseName = 'db_incident'
        collectionName = 'all_incidents'
    
        dataFrame = get_dataframe_from_mongo(databaseName, collectionName)
        return dataFrame[dataFrame.year == year]


def sort_dataframe_by(df, type):
    """
    sorts a given dataframe by its given type (if traffic_volume then sorts by volume, traffic_incident by count)
    :return: sorted dataframe
    """
    if type == 'traffic_volume':
        sortBy = 'volume'

    elif type == 'traffic_incident':
        sortBy = 'count'

    # Sort df
    return df.sort_values(by=sortBy, inplace=True)

def test():
    """
    demonstrating how to use the get dataframe dummy
    :return:
    """
    # drop_all_db()
    # ingest_data()
    # check_collection_in_dbs('2017_traffic_volume_flow')

    drop_all_db()
    ingest_data('C:/Users/burak/Desktop/Project_ENSF592/csv')

    #get_dataframe_from_db_by_year(2017, 'traffic_volume')
    print(get_dataframe_from_db_by_year(2017, 'traffic_incident'))
    
    # print(all_volumes)

if __name__ == "__main__":
    test()

