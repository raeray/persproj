import boto3
from boto.s3.connection import S3Connection
import boto
from boto.s3.key import Key
import sys
import os
import json
import pandas as pd
from collections import defaultdict
# import pyplot as plt
import ast 
sys.path.insert(0,os.path.abspath('..'))
from utils.credentials import access_key, secret_access_key

def make_category_list_column(df):
    df['categories_list'] = (df['categories']
    .apply(lambda x: x.split(',') if not pd.isnull(x) else None,1))
    return df

def count_categories(series, series_type='list'):
    '''
    put in series with all the categories
    example: 
    count_df = count_categories(business_df['categories_list'].values)
    '''
    count_dict = defaultdict(int)
    if series_type == 'list':
        for row in series:
            if row is not None or not pd.isnull(row):
                for item in row:
                    count_dict[item.strip()] += 1
    else:
        for row in series:
#             print(row, row is not None or pd.notna(row) or pd.notnull(row))
            if not pd.isnull(row) or not pd.isna(row):
                row = ast.literal_eval(row)
                for item in row.items():
                    count_dict[item[0].strip()] += 1
    res_df = pd.DataFrame.from_dict(count_dict, orient='index')
    res_df.rename(columns={0: 'count'}, inplace=1)
    return res_df.sort_values('count', ascending=False)

def get_restaurant_df(df):
    food_df = (df[
    (df['categories'].str.contains('Food',na=False)) |
     (df['categories'].str.contains('Restaurant',na=False))|
     (df['categories'].str.contains('Bar',na=False))
])
    return food_df
