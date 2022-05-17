import pandas as pd
from kafka import KafkaProducer
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
import json

TOPIC_NAME = "ddos_predictions"

def instantiate_kafka_producer():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        #value_serializer = lambda x: json.dumps(x).encode('utf-8')
    )
    
    if producer.bootstrap_connected():
        print(f"Successfully connected to bootstrap server")
    else:
        print("Couldn't connect to bootstrap server.")
        
    return producer

def __produce_message(producer_instance, topic, message):
    #df = pd.DataFrame([message])#.apply(lambda row: ','.join(row.values.astype(str)), axis=1)
    #producer_instance.send(topic, message)#bytes(str(df), encoding='utf-8')) #df.to_json()#bytes(str(message), 'utf-8'))
    
    # elastic_client = Elasticsearch(
    #     "http://localhost:9200", verify_certs = False
    # )
    # elastic_client = Elasticsearch(
    #     "https://localhost:9200",
    #     http_auth=("", ""), ca_certs = "D:\Program Files\elasticsearch-8.1.2\config\certs\http_ca.crt", verify_certs = False, client_cert = False, client_key = False
    # )

    #helpers.bulk(elastic_client, message, index = "ddos_predictions")
    #helpers.bulk(elastic_client, message, index = 'predictions')
    mm =  json.dumps(message).encode('utf-8')
    producer_instance.send(topic,mm)
    producer_instance.flush()
    return

def send_to_logstash(positive_prediction , producer, logger) :
        logger.info('Got an attatck.., Sending to Kafka..')
        #row = bytes(str(positive_prediction.data), encoding = "utf-8")
        #logger.info('\n\n\n\n\n' + row + '\n\n\n\n')
        __produce_message(producer, TOPIC_NAME, positive_prediction)#pd.DataFrame.from_dict((positive_prediction)).to_json(orient='records', lines=True))
        logger.info('sent to kafka')



        
           