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
        is_flow = (csv_file.find('Incidents') != -1)
        is_volume = (csv_file.find('Flow') != -1) or (csv_file.find('Volume') != -1)
        path = os.path.join(csv_key, csv_file)
        new_coll_name = Path(path).resolve().stem.lower()
        if is_csv and is_flow:
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
    creatimg an empty db
    :return:
    """
    mongo_client = pymongo.MongoClient(db_url, db_port)
    db_connection = mongo_client[db_name]


def drop_all_db(db_url='localhost', db_port=27017):
    mongo_client = pymongo.MongoClient(db_url, db_port)
    db_list = mongo_client.list_database_names()
    for i in db_list:
        is_user_db = (i.find('db') != -1)
        if is_user_db:
            mongo_client.drop_database(i)
            print('user db', i, 'is dropped')


def test():
    """
    demonstrating how to use the get dataframe dummy
    :return:
    """
    # drop_all_db()
    # ingest_data()
    # check_collection_in_dbs('2017_traffic_volume_flow')
    drop_all_db()
    ingest_data('../csv')


if __name__ == "__main__":
    test()
