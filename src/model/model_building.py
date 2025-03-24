import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
import yaml
from src.logger import logging

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

def train_model(X_train : np.ndarray ,y_train : np.ndarray) -> LogisticRegression:
    """ train the logistic regression model """
    try:
        clf = LogisticRegression(C= 1 , solver = 'liblinear' , penalty = 'l1')
        clf.fit(X_train , y_train)
        logging.info("Model training done")
        return clf 

    except Exception as e:
        logging.error("Error in training the model")
        raise 

    


def save_model(model, file_path: str) -> None:
    """Save the trained model to a file."""
    try:
        with open(file_path, 'wb') as file:
            pickle.dump(model, file)
        logging.info('Model saved to %s', file_path)
    except Exception as e:
        logging.error('Error occurred while saving the model: %s', e)
        raise

def main():
    try:
        train_data = load_data('./data/processed/train_bow.csv')
        X_train = train_data.iloc[:, :-1].values
        y_train = train_data.iloc[:, -1].values

        clf = train_model(X_train, y_train)
        
        save_model(clf, 'models/model.pkl')
    except Exception as e:
        logging.info("failed to complete the model building process ")
        raise 

if __name__ == "__main__":
    main()