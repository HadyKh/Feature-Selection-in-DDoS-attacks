# -*- coding: utf-8 -*-
from datetime import datetime
import logging
from dotenv import find_dotenv, load_dotenv
from libcst import Continue
from src.Kafka_server import malicious_logstach_ingestion, data_consumer
from src.models import predict_model, train_model
import pandas as pd
from kafka import KafkaConsumer
from os.path import exists

logstash_producer = malicious_logstach_ingestion.instantiate_kafka_producer()
consumer = data_consumer.instantiate_raw_data_consumer()
logstash_consumer = data_consumer.instantiate_logstash_consumer()

cols = ['Flow ID',	'Source IP','Source Port','Destination IP', 'Destination Port', 'Protocol', 'Timestamp', 'Flow Duration', 'Total Fwd Packets', 'Total Backward Packets','Total Length of Fwd Packets', 'Total Length of Bwd Packets',
'Fwd Packet Length Max','Fwd Packet Length Min', 'Fwd Packet Length Mean', 'Fwd Packet Length Std','Bwd Packet Length Max', 'Bwd Packet Length Min', 'Bwd Packet Length Mean', 'Bwd Packet Length Std',	'Flow Bytes/s',	'Flow Packets/s',
'Flow IAT Mean', 'Flow IAT Std','Flow IAT Max', 'Flow IAT Min','Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Std', 'Fwd IAT Max', 'Fwd IAT Min','Bwd IAT Total', 'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min','Fwd PSH Flags',
'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 'Fwd Header Length', 'Bwd Header Length','Fwd Packets/s', 'Bwd Packets/s', 'Min Packet Length', 'Max Packet Length', 'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance',
'FIN Flag Count', 'SYN Flag Count','RST Flag Count','PSH Flag Count', 'ACK Flag Count', 'URG Flag Count', 'CWE Flag Count', 'ECE Flag Count', 'Down/Up Ratio', 'Average Packet Size', 'Avg Fwd Segment Size', 'Avg Bwd Segment Size', 
'Fwd Header Length.1','Fwd Avg Bytes/Bulk', 'Fwd Avg Packets/Bulk', 'Fwd Avg Bulk Rate','Bwd Avg Bytes/Bulk','Bwd Avg Packets/Bulk','Bwd Avg Bulk Rate','Subflow Fwd Packets','Subflow Fwd Bytes','Subflow Bwd Packets','Subflow Bwd Bytes',
'Init_Win_bytes_forward','Init_Win_bytes_backward','act_data_pkt_fwd','min_seg_size_forward','Active Mean','Active Std','Active Max','Active Min','Idle Mean','Idle Std','Idle Max','Idle Min','SimillarHTTP','Inbound','Label']


def main(): 
    logger = logging.getLogger(__name__)
    logger.info('===Checking models availability')
    
    #checking for the model existance
    file_exists = exists('../../models/cb_model.pkl')
    if file_exists: # checking if the pickled model is exist in the  specified path
        logger.info('===Your model is ready')
        Continue
    else: # if the model is not exist in the specified path it will train and pickle a new model
        logger.info('===Training catboost classifier..') 
        train_model.train_and_pickle() # training model
        logger.info('=== model trained successfuly')
    
    logger.info('===Consumer successfully initialized')
    for data in consumer:
        logger.info('===Reading Data')

        data_df = pd.DataFrame([data.value.decode('utf-8').split(',')], columns = cols)
        logger.info('===Load Model & predict')
        data_df['pred'], data_df['confidence'] = predict_model.predict_cb(data_df, logger)

        logger.info('===Successfully predicted\n')
        

        if data_df['pred'][0] == 1:
            logger.info('===sending to logstash\n')
            # temp_df = pd.DataFrame()
            # temp_df['data'] = data_df[data_df.columns].apply(lambda row: ','.join(row.values.astype(str)), axis=1)
            ip = data_df['Source IP'].values
            prot = data_df['Protocol'].values
            dest_port = data_df['Destination Port'].values
            pred = data_df['pred'].values
            conf = data_df['confidence'].values

            to_produce = {
                'timestamp': str(datetime.now().isoformat()),
                'Source IP': str(ip[0]),
                'Protocol': str(prot[0]),
                'Destination Port': str(dest_port[0]),
                'model': 'Catboost Classifier',
                'prediction_score': str(pred[0]),
                'Confidence_Score': str(conf[0])

            }
            malicious_logstach_ingestion.send_to_logstash(to_produce, logstash_producer, logger)
        logger.info('===Saving Logs to CSV file\n')
        with open('../../data/processed/all_output_dataset.csv', encoding='utf-8', mode='a') as f: 
            data_df.to_csv(f, index=False, header=f.tell()==0, line_terminator='\n')
        logger.info('=== CSV file written')





if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # # not used in this stub but often useful for finding various files
    #project_dir = Path(__file__).resolve().parents[2]
    # find .env automagically by walking up directories until it's found, then
    
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()






