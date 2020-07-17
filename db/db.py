"""
https://docs.mongodb.com/drivers/pymongo
please make sure mongod is active before running this module
"""
import os
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
    # db_collection.delete_many({})
    db_collection.insert_many(payload)
    print('csv file', '\'' + collection_name + '\'', ' is imported in \'', db_name, '\' database')


def drop_collection(db_name, collection_name, db_url, db_port):
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


def create_db(db_name, collection_name, db_url, db_port):
    """
    creatimg an empty db
    :return:
    """
    mongo_client = pymongo.MongoClient(db_url, db_port)
    db_connection = mongo_client[db_name]


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


def test():
    """
    demonstrating how to use the get dataframe dummy
    :return:
    """
    filepath = 'csv/'+'2017_Traffic_Volume_Flow.csv'
    data = get_dataframe_from_mongo_dummy(filepath)
    print(data)

    # db_url = 'localhost'
    # db_port = 27017
    # import_csv_to_db(filepath, 'db', '2017_Traffic_Volume', db_url, db_port)
    # print_collection('db', '2017_Traffic_Volume', db_url, db_port)
    # drop_collection('db', '2017_Traffic_Volume', db_url, db_port)
    # drop_collection('db', '2017_Traffic_Volume', db_url, db_port)
    # print_collection('db', '2017_Traffic_Volume', db_url, db_port)


def get_dataframe_from_mongo_dummy(csv_path):
    """
    will return a dataframe which will be the exactly the same as the real one
    read from mongodb
    :return: a dummy dataframe
    """
    absolute_path = os.path.abspath(__file__)
    current_path = os.path.dirname(absolute_path)
    os.chdir(current_path)
    data = pd.read_csv(csv_path)
    return data


if __name__ == "__main__":
    test()
