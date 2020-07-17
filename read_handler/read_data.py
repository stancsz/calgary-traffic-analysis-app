import os

from db import db


def main():
    db.ingest_data('../csv')  # Note that ingest data only need to run once
    data = db.get_dataframe_from_mongo('db_volume', 'trafficflow2016_opendata')
    """
    A list of possible collections & dbs
        Collection:  '2017_traffic_volume_flow'  is imported in DB: 'db_volume'
        Collection:  'traffic_incidents'  is imported in DB: 'db_incident'
        Collection:  'trafficflow2016_opendata'  is imported in DB: 'db_volume'
        Collection:  'traffic_incidents_archive_2017'  is imported in DB: 'db_incident'
        Collection:  'traffic_incidents_archive_2016'  is imported in DB: 'db_incident'
        Collection:  'traffic_volumes_for_2018'  is imported in DB: 'db_volume'
    """
    print(data)


if __name__ == '__main__':
    main()
