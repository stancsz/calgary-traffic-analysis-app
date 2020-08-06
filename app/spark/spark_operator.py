from pyspark.shell import sqlContext
from pyspark.sql import SparkSession
import pandas as pd
# project modules
from app.database.db import get_dataframe_from_mongo
# https://intellipaat.com/community/7658/convert-pyspark-string-to-date-format
# TO-DOS: parse datetime into datetime, currently typed as type double

def spark_init():
    """
    to eliminate import error
    https://stackoverflow.com/questions/37513355/converting-pandas-dataframe-into-spark-dataframe-error
    :return:
    """
    spark = SparkSession.builder.appName("pandasToSparkDF").getOrCreate()
    sc = spark.sparkContext
    return spark, sc


from pyspark.sql.types import *

# Auxiliar functions
def equivalent_type(f):
    if f == 'datetime64[ns]': return DateType()
    elif f == 'int64': return LongType()
    elif f == 'int32': return IntegerType()
    elif f == 'float64': return FloatType()
    else: return StringType()

def define_structure(string, format_type):
    try: typo = equivalent_type(format_type)
    except: typo = StringType()
    return StructField(string, typo)


# Given pandas dataframe, it will return a spark's dataframe.
def pandas_to_spark(pandas_df):
    columns = list(pandas_df.columns)
    types = list(pandas_df.dtypes)
    struct_list = []
    for column, typo in zip(columns, types):
      struct_list.append(define_structure(column, typo))
    p_schema = StructType(struct_list)
    return sqlContext.createDataFrame(pandas_df, p_schema)


def main():
    pdf_vol = get_dataframe_from_mongo("db_volume", "all_volumes")
    pdf_inc = get_dataframe_from_mongo("db_incident", "all_incidents")
    # print(pdf_vol.columns)
    # print(pdf_inc.columns)
    print(pdf_vol.loc[1])
    print(pdf_inc.loc[1])

    vol_schema = StructType([StructField("segment_name", StringType(), True) \
                                , StructField("year", IntegerType(), True) \
                                , StructField("the_geom", StringType(), True) \
                                , StructField("length_m", DoubleType(), True) \
                                , StructField("volume", IntegerType(), True)
                             ])
    inc_schema = StructType([StructField("incident_info", StringType(), True) \
                                , StructField("description", StringType(), True) \
                                , StructField("start_dt", StringType(), True) \
                                , StructField("modified_dt", StringType(), True) \
                                , StructField("year", IntegerType(), True) \
                                , StructField("quadrant", StringType(), True) \
                                , StructField("latitude", DoubleType(), True) \
                                , StructField("longitude", DoubleType(), True) \
                                , StructField("location", StringType(), True) \
                                , StructField("count", IntegerType(), True) \
                                , StructField("grid_num", IntegerType(), True)
                             ])

    spark, sc = spark_init()
    sdf_vol = spark.createDataFrame(pdf_vol, schema=vol_schema)
    sdf_inc = spark.createDataFrame(pdf_inc, schema=inc_schema)
    print(type(sdf_vol))
    print(type(sdf_inc))


if __name__ == '__main__':
    main()
