from kafka import KafkaConsumer

def instantiate_raw_data_consumer():
    consumer = KafkaConsumer( 
        'raw_ddos_csv',
        bootstrap_servers = ['localhost:9092'],
        auto_offset_reset = 'earliest',
        enable_auto_commit = False
    )
    return consumer

def instantiate_logstash_consumer():
    consumer = KafkaConsumer( 
        'ddos_predictions',
        bootstrap_servers = ['localhost:9092'],
        auto_offset_reset = 'earliest',
        enable_auto_commit = False
    )
    return consumer