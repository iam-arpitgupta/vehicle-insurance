# feature engineering 
import numpy as np 
import pandas as pd 
import os 
import yaml 
from src.logger import logging 
import pickle
from sklearn.feature_extraction.text import CountVectorizer

def load_data(file_path : str)-> pd.DataFrame:
    """Load the data form the csv file """
    try:
        df = pd.read_csv(file_path)
        df.fillna('',inplace = True)
        return df 
    except pd.errors.ParserError as e:
        logging.error('Failed to parse the CSV file: %s', e)
        raise
    except Exception as e:
        logging.error("error in loading the data %s",e)
        raise 


def apply_bow(train_df : pd.DataFrame , test_df : pd.DataFrame , max_features : int)-> tuple:
    """
    Apply Count vectorizer to the data 
    """
    try:
        logging.info("Applying Bow")

        vectorizer = CountVectorizer(max_features = max_features)

        X_train = train_data['review'].values 
        y_train = train_data['sentiment'].values 
        X_test = test_data['review'].values 
        y_test = test_data['sentiment'].values 

        X_train_bow = vectorizer.fit_transform(X_train)
        X_test_bow = vectorizer.transform(X_test)

        train_df = pd.DataFrame(X_train_bow.toarray())
        train_df['label'] = y_train

        test_df = pd.DataFrame(X_test_bow.toarray())
        test_df['label'] = y_test

        pickle.dump(vectorizer , open('models/vectorizer.pkl','wb'))
        logging.info('Bow applied and saved ')
        return train_df , test_df
    
    except Exception as e:
        logging.error('could not apply bow : %s',e)
        raise 


def save_data(df: pd.DataFrame, file_path: str) -> None:
    """Save the dataframe to a CSV file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        logging.info('Data saved to %s', file_path)
    except Exception as e:
        logging.error('Unexpected error occurred while saving the data: %s', e)
        raise

def main():
    try:
        train_data = load_data("data/interim/train_processed.csv")
        test_data = load_data("data/interim/test_processed.csv")
        max_features = 20

        train_df, test_df = apply_bow(train_data, test_data, max_features)

        save_data (train_df ,  os.path.join("./data", "processed", "train_bow.csv"))
        save_data(test_df, os.path.join("./data", "processed", "test_bow.csv"))

    except Exception as e:
        logging.erro('failed to complete the preprocessing : %s',e)
        raise 


if __name__ == "__main__":
    main()






