import pandas as pd
from kafka import KafkaProducer
from datetime import datetime

TOPIC_NAME = "raw_ddos_csv"

def instantiate_kafka_producer():
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
    )
    
    if producer.bootstrap_connected():
        print(f"Successfully connected to bootstrap server")
    else:
        print("Couldn't connect to bootstrap server.")
        
    return producer

def produce_message(producer_instance, topic, message):
    producer_instance.send(topic, message)
    producer_instance.flush()
    return

if __name__ == "__main__":

    producer = instantiate_kafka_producer()
    
    print("Ingesting the Data in Batches of 10000")
    
    for batch_id, data_batch in enumerate(pd.read_csv("../../data/interim/testing_prod.csv", chunksize=10000)):
        start_time = datetime.now()
        print(f"Ingesting Batch: {batch_id}")

        for idx, instance in data_batch.iterrows():
            domain = bytes(instance.combined, encoding="utf-8")
            produce_message(producer_instance=producer, topic=TOPIC_NAME, message=domain)

        end_time = datetime.now()
        print(f"Batch {batch_id} took {end_time-start_time} time for ingesting data")

    print("Ingestion Completed")