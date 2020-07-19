"""
https://docs.mongodb.com/drivers/pymongo
please make sure mongod is active before running this module
"""
import os
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
    for csv_file in os.listdir(csv_key):
        is_csv = (csv_file.endswith(".csv"))
        is_incident = (csv_file.find('Incidents') != -1)
        is_volume = (csv_file.find('Flow') != -1) or (csv_file.find('Volume') != -1)
        path = os.path.join(csv_key, csv_file)
        new_coll_name = Path(path).resolve().stem.lower()
        if is_csv and is_incident:
            import_csv_to_db(path, 'db_incident', new_coll_name)
        elif is_csv and is_volume:
            import_csv_to_db(path, 'db_volume', new_coll_name)
        else:
            continue


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
    creatimg an empty database
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

    ## Traffic Flow Dataframe
    all_volumes = pd.DataFrame()
    collections_volume = ['2017_traffic_volume_flow','traffic_volumes_for_2018','trafficflow2016_opendata']
    
    for collection in collections_volume:
        ### start reading collection
        dataFrame = get_dataframe_from_mongo('db_volume', collection, db_url='localhost', db_port=27017)

        # renaming column headers to standardized names
        if collection == collections_volume[0]:
            # for 2017_traffic_volume_flow, column order is # year | segment_name | the_geom | length_m | volume
            dataFrame.columns = ['year', 'segment_name', 'the_geom', 'length_m', 'volume']
        elif collection == collections_volume[1]:
            # for traffic_volumes_for_2018, column order is # YEAR | SECNAME | Shape_Leng | VOLUME | multilinestring
            dataFrame.columns = ['year', 'segment_name', 'length_m', 'volume', 'the_geom']
        elif collection == collections_volume[2]:
            # for trafficflow2016_opendata, column order is # secname | the_geom | year_vol | shape_leng | volume
            dataFrame.columns = ['segment_name', 'the_geom', 'year', 'length_m', 'volume']

        # re-ordering dataframe columns
        df = dataFrame.reindex(columns= ['segment_name', 'year', 'the_geom', 'length_m', 'volume'])

        # ignore index is to re-index all entries when merging (so that 2nd collection entries do not start from 0)
        all_volumes = pd.concat([all_volumes, df], ignore_index=True)



    ## Incidents Dataframe
    all_incidents = pd.DataFrame()
    collections_incidents = ['traffic_incidents','traffic_incidents_archive_2016','traffic_incidents_archive_2017']

    for collection in collections_incidents:
        ### start reading collection
        dataFrame = get_dataframe_from_mongo('db_incident', collection, db_url='localhost', db_port=27017)

        if collection == collections_incidents[0]:
            # we don't have id column on the other collections so dropping that
            del dataFrame['id']
            # for traffic_incidents,                column order is # INCIDENT INFO | DESCRIPTION | START_DT | MODIFIED_DT | QUADRANT | Longitude | Latitude | location | Count | id
            # for traffic_incidents_archive_2016,   column order is # INCIDENT INFO | DESCRIPTION | START_DT | MODIFIED_DT | QUADRANT | Longitude | Latitude | location | Count 
            # for traffic_incidents_archive_2017,   column order is # INCIDENT INFO | DESCRIPTION | START_DT | MODIFIED_DT | QUADRANT | Longitude | Latitude | location | Count 

        # renaming column headers to standardized names
        dataFrame.columns = ['incident_info', 'description', 'start_date', 'modified_date', 'quadrant', 'longitude', 'latitude', 'location', 'count']

        # re-ordering dataframe columns
        df = dataFrame.reindex(columns= ['incident_info', 'description', 'start_date', 'modified_date', 'quadrant', 'longitude', 'latitude', 'location', 'count'])
    
        # ignore index is to re-index all entries when merging (so that 2nd collection entries do not start from 0)
        all_incidents = pd.concat([all_incidents, df], ignore_index=True)

    drop_all_db()

    # import unified collections into db
    import_dataframe_to_db(all_volumes, 'db_volume', 'all_volumes')
    import_dataframe_to_db(all_incidents, 'db_incident', 'all_incidents')

    # Sort all volumes by volume
    all_volumes.sort_values(by='volume', inplace=True)

    print(all_volumes)

if __name__ == "__main__":
    test()
