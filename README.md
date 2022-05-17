# Feature-Selection-in-DDoS-attacks
The effect of using Feature selection techniques against DDoS attacks

# Introduction
DDoS attacks is one of the security challenges that threat the availability of any system. Distributed Denial of service attacks “DDoS” is a systematic attack that targets a corporation servers or network with a huge number of requests, that exceeds the computational power of the server, causing the server to be down and sometimes it get the whole network down. One of the most effective proposed solutions is using machine learning to detect the malicious traffic that leads to discover if the network is under attack.
 Since the data used is a high dimensional data, and to avoid the trap of the high dimensional data known as curse of dimensionality. So, we need to decrease these dimensions in a scientific reasonable approach. As this high dimensional data may considered as misleading for the model. Feature selection techniques is an important approach to consider, as it will help us to depend only on the most important features that, which will help in reduce the time needed and the computational cost for the problem being solved. It also helps to increase the performance in the mean of accuracy and efficiency
 
 # Feature Selection Techniques used
- Univariate selection, 
- Feature importance, 
- correlation matrix with heatmaps,
- SHAP (Lundberg, 2018) for feature selection.

Comparing all of these techniques will give an intuition of how feature selection is important, and the most important features that can be used to help in defending against the DDoS attack

# machine Learning model used
Catboost Classifier

# final used model
SHAP feature selection + Catboost Classifier. with accuracy of 0.99980, F1-Score of 0.99990 and prediction time of 0.000242 ms.

# ELk Stack
ELK stack is composed of three main architectures, logstash, Elasticsearch and kibana. 
Elastic search engine is a distributed search and analytics engine. Logstash data collection and indexing tool, collect and index data to elasticsearch. Kibana is the last step of ELK stack, responsible for data analysis and visualization through interactive dashboards, diagrams and graphs. Mainly the architecture is as follows: logstash as an indexer or data aggregator to index the data to the elasticsearch as a storage stage that can be analyzed and visualized in kibana.

# Dataset used for training
CICDDoS2019. Contains benign and the most up-to-date common DDoS attacks, which resembles the true real-world data (PCAPs). It also includes the results of the network traffic analysis using CICFlowMeter-V3 with labeled flows based on the time stamp, source, and destination IPs, source and destination ports, protocols and attack (CSV files). The dataset has been organized per day. For each day, they recorded the raw data including the network traffic (Pcaps) and event logs (windows and Ubuntu event Logs) per machine. In the features extraction process from the raw data, they used the CICFlowMeter-V3 and extracted more than 80 traffic features and saved them as a CSV file per machine. can be found here: https://www.unb.ca/cic/datasets/ddos-2019.html.


