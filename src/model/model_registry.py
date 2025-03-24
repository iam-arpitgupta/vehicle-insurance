import json 
import mlflow 
import logging 
from src.logger import logging 
import os 
import dagshub 

import warnings
warnings.simplefilter("ignore", UserWarning)
warnings.filterwarnings("ignore")


# set the dagshub token
dagshub_token = os.getenv("CAPSTONE_TEST")
if not dagshub_token:
    raise EnvironmentError("CAPSTONE_TEST environment variable not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

dagshub_url = "https://dagshub.com"
repo_owner = "vikashdas770"
repo_name = "YT-Capstone-Project"
# Set up MLflow tracking URI
mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

def load_model_info(file_path : str) -> dict:
    """Load the model of the json file"""
    try:
        with open(file_path , 'r') as  file:
            model_info= json.load(file)
        logging.debug(" what is the loaded form %s",file_path)
        return model_info
    except FileNotFoundError:
        logging.error('File not found: %s', file_path)
        raise  
    except Exception as e:
        logging.error("unexpected model occured hile loading the model info %s",e)
        raise 

def register_model(model_name : str , model_info : dict):
    """register the model to the mlflow model registry """
    try:
        model_uri = f"runs:/{model_info['run_id']}/{model_info['model_path']}"

        # register the model 
        model_version = mlflow.register_model(model_uri , model_name)

        # transition the model to the model stage 
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name = model_name , 
            version = model_version.version ,
            stage = "Staging"
        )
        logging.debug(f'Model {model_name} version {model_version} registered and transition to the Staging ')
    except Exception as e:
        logging.error('Error model is registerd %s' , e)
        raise 


def main():
    try: 
        model_info_path = 'reports/experiment_info.json'
        model_info = load_model_info(model_info_path)

        model_name = "my_model"

        register_model(model_info,model_name)

    except Exception as e:
        logging.error('Failed to complete the model registration process: %s', e)
        print(f"Error: {e}")

if __name__ == "__main__":
    main()    
