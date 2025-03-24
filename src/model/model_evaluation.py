import numpy as np 
import pandas as pd 
import pickle
import json 
from sklearn.metrics import accuracy_score , precision_score , recall_score , roc_auc_score 
import logging 
import mlflow
import dagshub 
import mlflow.sklearn 
from src.logger import logging 
import os 


# set up the dagshub credentials using mlflow tracking 
dagshub_token = os.getenv("CAPSTONE TEST")
if not dagshub_token:
    raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

dagshub_url = "https://dagshub.com"
repo_owner = "arpit09"
repo_name = "YT-Capstone-Project"




# Set up MLflow tracking URI
mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

# below  code is for local use 



def load_model(file_path : str):
    """Load the model Logistic model """
    try:
        with open(file_path , 'r') as file:
            model = pickle.load(file)
        logging.info("loaded the model")
        return model 
    except FileNotFoundError:
        logging.error('File not found: %s', file_path)
        raise
    except Exception as e:
        logging.info("couldn't load the model")
        raise 


def load_data(file_path : str)-> pd.DataFrame:
    """ Load the data from the csv file """
    try:
        df = pd.read_csv(file_path)
        logging.info('Data loaded from %s', file_path)
        return df
    except pd.errors.ParserError as e:
        logging.error('Failed to parse the CSV file: %s', e)
        raise
    except Exception as e:
        logging.error('Unexpected error occurred while loading the data: %s', e)
        raise

def evaluate_model(clf, X_test:np.ndarray , y_test :np.ndarray) -> dict:
    """ Evaluate the model and return the evaluation metrics """
    try: 
        y_pred = clf.predict(X_test)
        y_pred_proba = clf.predict_proba(X_test)[:,1]

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred_proba)

        metrics_dict = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'auc': auc
        }
        logging.info('Model evaluation metrics calculated')
        return metrics_dict
    
    except Exception as e :
        logging.error("failed to do the evaluation part ")
        raise 

def save_metrics(metrics : dict , file_path : str )-> None:
    """ save the evaluation metrics  with  the json file """
    try:
        with open(file_path, 'w') as file:
            json.dump(metrics, file, indent=4)
        logging.info('Metrics saved to %s', file_path)
    except Exception as e:
        logging.error("error occured while saving the file")
        raise 

def save_model_info(run_id : str , model_path : str , file_path : str)-> None:
    """Save the model run ID nd path to the json file """
    try:
        model_info = {'run_id' : run_id , 'model_path' : model_path}
        with open(file_path , 'w') as file:
            json.dump(model_info , file , indent = 4)
        logging.info*('saved the model info %s',file_path)

    except Exception as e:
        logging.error("Error occured while saving the model ")
        raise 

def main():
    mlflow.set_experiment("my-dvc pipeline")
    with mlflow.start_run() as run:
        try:
            clf = load_model('./models/models.pkl')
            test_data = load_data('./data/processed/test_bow.csv')

            X_test = test_data.iloc[:,:-1].values
            y_test = test_data.iloc[: , -1].values 

            metrics = evaluate_model(clf, X_test , y_test)
            save_metrics(metrics, 'reports/metrics.json')

            # log the metrics 
            with metric_name , metric_value in metrics.items():
                mlflow.log_metrics(metric_name , metric_value)

            # Log model parameters to MLflow
            if hasattr(clf, 'get_params'):
                params = clf.get_params()
                for param_name, param_value in params.items():
                    mlflow.log_param(param_name, param_value)
            
            # Log model to MLflow
            mlflow.sklearn.log_model(clf, "model")
            
            # Save model info
            save_model_info(run.info.run_id, "model", 'reports/experiment_info.json')
            
            # Log the metrics file to MLflow
            mlflow.log_artifact('reports/metrics.json')


        except Exception as e:
            logging.error('Failed to complete the model evaluation process: %s', e)
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
