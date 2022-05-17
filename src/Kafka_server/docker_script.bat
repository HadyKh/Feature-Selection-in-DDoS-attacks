docker-compose -f docker-compose.yml up -d
docker-compose -f docker-elastic-search-kibana.yml up -d
docker pull elasticdump/elasticsearch-dump

rem timeout /t 5
docker exec kafka /bin/bash -c "cd /opt/kafka/bin; kafka-topics.sh --create --topic raw_ddos_csv --bootstrap-server localhost:9092"
docker exec kafka /bin/bash -c "cd /opt/kafka/bin; kafka-topics.sh --create --topic ddos_predictions --bootstrap-server localhost:9092"
pip install -r requirements.txt
python data_ingestion_script.py
