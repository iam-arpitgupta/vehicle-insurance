import numpy as np 
import pandas as pd
import os 
from sklearn.model_selection import train_test_split 
import yaml 
import logging 
from src.logger import logging
from src.connections import s3_connection 


# read the params from the yaml file 
def load_params(params_path : str) -> dict:
    """load parameters from the yaml file """
    try:
        with open(params_path , 'r') as file:
            params = yaml.safe_load(file)
        logging.debug('Parameters retireved from %s' ,params_path)
        return params
    except FileNotFoundError:
        logging.error('file not found: %s',params)
        raise 
    except yaml.YAMLError as e:
        logging.error("YAML ERROR : %s",e)
    except Exception as e:
        logging.error('Unexpected Error : %s',e)
        raise 


def load_data(data_url : str) -> pd.DataFrame:
    """load the data from the csv file"""
    try:
        df = pd.read_csv(data_url)
        logging.debug("loaded the csv data %s" , data_url)
        return df
    except pd.error.ParseError as e:
        logging.error('parse error L %s' , e)
        raise 
    except Exception as e:
        logging.error('Could not load the file : %s',e)
        raise 

def preprocess_data(df : pd.DataFrame) -> pd.DataFrame:
    """ preprocess the data"""
    try:
        logging.info("pre-processing")
        final_df = df[df['sentiment'].isin(['positive','negative'])]
        final_df['sentiment'] = final_df['sentiment'].replace({'positive': 1, 'negative': 0})
        logging.info('Data preprocesssing completed')
        return final_df
    except KeyError as e:
        logging.info('Missing data in dataframe:%s',e)
        raise 
        
    except Exception as e:
        logging.error('could not preprocess the data %s',e )
        raise 


def save_data(train_data : pd.DataFrame , test_data : pd.DataFrame , data_path : str) -> None:
    try:
        raw_data_path = os.path.join(data_path , 'raw')
        os.makedirs(raw_data_path , exist_ok=True)
        train_data.to_csv(os.path.join(raw_data_path , 'train.csv'),index = False)
        test_data.to_csv(os.path.join(raw_data_path , 'train.csv'),index = False)
        logging.debug("data saved %s" , raw_data_path)
    except Exception as e:
        logging.error("unexpected error while saving the data %s" , e)
        raise 

def main():
    try:
        # it will take all the data from tha params part 
        params = load_params('params.yaml')
        test_size = params['data_ingestion']['test_size']
        #test_size = 0.2

        #df = load_data(data_url = )
        s3 = s3_connection.s3_operations(final_df, test_size = test_size , random_state = 42)
        df = s3.fetch_files_from_s3("data.csv")

        final_df = preprocess_data()
        train_data , test_data = train_test_split(final_df , test_size = test_size , random_state =42)
        save_data(train_data , test_data , data_path= './data')
    except Exception as e:
        logging.error('failed to completed the data ingestion %s' , e)
        raise 

if __name__ == '__main__':
    main()

