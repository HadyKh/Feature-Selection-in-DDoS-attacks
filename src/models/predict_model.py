import pickle
import numpy as np


def __preprocess_data(df):
    """preprocessing data to used in fitting
    parameters:
        df: dataframe containing data to fit on
    Return:
        df: dataframe containing preprocessed data
    """
    df = df[['Fwd Packet Length Max', 'min_seg_size_forward', 'Inbound', 'URG Flag Count', 'Fwd PSH Flags', 'Flow IAT Mean']]
    return df

def predict_cb(data, logger):
    """Loading the catboost classifier predict_proba
    parameters:
        df: dataframe containing data to fit on
        logger: the identified logger to logging the steps
    Return:
        pred[]: the prediction 
        confidence_score: the confidence score
    """
    data = __preprocess_data(data) # dropping the unsused columns

    logger.info('===model is loading..')
    model = pickle.load(open('../../models/cb_model.pkl', 'rb')) # load the pickling the model
    logger.info('===predicting')

    pred_proba = model.predict_proba(data) # predicting the confidence score
    index = np.unravel_index(np.argmax(pred_proba, axis=None), pred_proba.shape) # getting the index of the maximum probability
    confidence_score = pred_proba[index] # getting the score
    pred = np.argmax(pred_proba, axis=1) # getting the predictions

    logger.info('===predicted successfully')

    return pred[0], confidence_score