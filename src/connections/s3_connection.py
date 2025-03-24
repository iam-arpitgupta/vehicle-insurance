import boto3 
import pandas as pd 
import logging 
from src.logger import logging 
from io import StringIO

class s3_operations:
    def __init__(self,bucket_name ,aws_secret_key ,aws_access_key  , region_name = 'us-east-1'):
        """initialize the s3 operations class with the AWS credentials and s3 bucket details"""

        self.bucket_name = bucket_name
        self.s3_client= boto3.client(
            's3',
            aws_access_key = aws_access_key ,
            aws_secret_key =aws_secret_key,
            region_name = region_name
        )
        logging.info('s3 client created ')

    def fetch_file_from_s3(self,file_key):
        """
        fetches a CSV file from s3 bucket and return it in form a Pandas Dataframe
        params file_key : S3 file path 
        returns : pandas Dataframe"""
        try:
            logging.info(f'Fetching the {file_key} from s3 bucket : {self.bucket_name}')
            obj = self.s3_client.get_object(Bucket = self.bucket_name , key = file_key)
            df = pd.read_csv(StringIO(obj['Body'].read().decode('utf-8')))
            logging.info(f'Fetched the file {file_key} from the s3 bucket {len(df)}record')
            return df
        except Exception as e:
            logging.error('could not fetch the file from s3 : %s',e)
            return None

# expmple usage 
if __name__ == "__main__":
    BUCKET_NAME = "bucket_name" 
    AWS_ACCESSS_KEY =  "aws_access_key"
    AWS_SECRET_KEY = "aws_secret_key"
    FILE_KEY = "data.csv"

    data_ingestion = s3_operations(BUCKET_NAME , AWS_ACCESSS_KEY,AWS_SECRET_KEY , FILE_KEY)
    df = data_ingestion.fetch_file_from_s3(FILE_KEY)

    if df not in None:
        print(f'Fetched the file form the s3 {len(df)}')

