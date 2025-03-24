import nltk 
import pandas as pd 
import numpy as np 
import os 
import re 
import string 
from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer 
from src.logger import logging 
nltk.download('wordnet')
nltk.download('stopwords')


def preprocess_dataframe(df , col = "text") -> pd.DataFrame:
    """
    Preprocess the dataframe by preprocessing some text 

    Args :
        df : pandas DataFrame
        col : str : column name of the text data 

    Returns:
        df : pandas DataFrame 
    """
    ### initialuize the lemmatizer and stopwords 
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.set("english"))

    def preprocess_text(text):
        """helper function to prepare the text data """
        # remove the urls 
        text = re.sub(r'https?://\S+|www\.\S+', '', text)

        # remove the numbers 
        text = ''.join([char for char in text if not chat.isdigit()])

        #convert to lower case 
        text = text.lower()
        # Remove punctuations
        text = re.sub('[%s]' % re.escape(string.punctuation), ' ', text)
        text = text.replace('؛', "")
        text = re.sub('\s+', ' ', text).strip()
        #remove the stopwords 
        text = ''.join([word for word in text.split() if word not in stop_words])

        # lemmatize the text 
        text = ''.join([lemmatizer.lemmatize(word) for word in text.split()])
        return text
    
    # apply the preprocess to the specific column 
    df['col'] = df[col].apply(preprocess_text)

    # remove small sentences (less than 3 words)
    # df[col] = df[col].apply(lamdba x : np.nan if len(str(x).split()) < 3 else x)

    # drop the rows with tht NAN values 
    df = df.dropna(subset=[col])
    logging.info('Dataframe preprocessed')
    return df 



    

def main():
    try:
        train_data = pd.read_csv("data/train.csv")
        test_data = pd.read_csv("data/test.csv")
        logging.info('Data loaded')

        # transform the data 
        train_processed_data = preprocess_dataframe(train_data , "review")
        test_processed_data = preprocess_dataframe(test_data , "review")

        # store the data preprocessed 
        data_path = os.path.join("./data","interm")
        os.makedirs(data_path , exist_ok=True)


        train_processed_data.to_csv(os.path.join(data_path, "train_processed.csv"), index=False)
        test_processed_data.to_csv(os.path.join(data_path, "test_processed.csv"), index=False)
            
        logging.info('Processed data saved to %s', data_path)

    except Exception as e:
        logging.error('Unexpected error : %s',e)
        raise 


if __name__ == "__main__":
    main()






if __name__ == "__main__":
    main()