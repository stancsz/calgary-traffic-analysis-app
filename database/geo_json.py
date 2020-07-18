from database.db import get_dataframe_from_mongo_dummy
from geojson import MultiLineString
import re
from pymongo import *


def parse_multiline_string(multiline_string):
    """
    MULTILINESTRING ((-114.0701479559 51.0485978122,
    -114.0691867156 51.0485664617,
    -114.0683208229 51.0485461436,
    -114.067765683 51.0485289854))
    """
    coordinate_list = re.split(r"[\[\]\(\),]", multiline_string)
    coordinate_list = list(filter(None, coordinate_list))
    for index, elem in enumerate(coordinate_list):
        if re.search('[a-zA-Z]', coordinate_list[index]):
            coordinate_list.pop(index)
    return_coordinates = []
    for i in coordinate_list:
        try:
            values = i.split()
            # print(values[0], values[1])
            return_coordinates.append([float(values[1]), float(values[0])])  # the database coordinates is flipped
        except:
            continue
    # print(return_coordinates)
    return return_coordinates

    # print(coordinate_list)


def get_geo_json(coordinates):
    geo_json = MultiLineString(coordinates)
    return geo_json


def get_geo_json_form_df(geo_df, index):
    geo_raw = geo_df[index]
    coordinates = parse_multiline_string(geo_raw)
    return get_geo_json(coordinates)


def get_geo_df(source_data_frame, the_geom_name):
    geo_df = source_data_frame[the_geom_name]
    return geo_df


def test():
    df = get_dataframe_from_mongo_dummy('../csv/2017_Traffic_Volume_Flow.csv')
    src_geo_df = get_geo_df(df, 'the_geom')
    # print(src_geo_df)
    for index, values in enumerate(src_geo_df):
        geojson = get_geo_json_form_df(src_geo_df, index)


if __name__ == '__main__':
    test()
