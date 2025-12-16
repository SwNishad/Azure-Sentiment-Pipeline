## ☁️ Real-Time Sentiment Analysis Pipeline on Azure

![Status](https://img.shields.io/badge/Status-Completed-success)
![Azure](https://img.shields.io/badge/Azure-Event%20Hubs%20|%20Databricks-blue)
![Spark](https://img.shields.io/badge/Apache%20Spark-Structured%20Streaming-orange)
![PowerBI](https://img.shields.io/badge/Visualization-Power%20BI-yellow)


## 📌 Project Overview
In the age of high-frequency social media and e-commerce, businesses cannot afford to wait for daily batch jobs to understand customer sentiment. This project implements a **Real-Time Data Engineering Pipeline** that ingests, processes, and visualizes simulated user reviews instantly.

**Goal:** Transform raw, unstructured text streams into actionable business intelligence with sub-second latency.

**Key Features:**
* **High-Throughput Ingestion:** Capable of handling thousands of events per second via Azure Event Hubs.
* **Real-Time NLP:** Uses Spark Structured Streaming and Python's `TextBlob` to calculate sentiment polarity on the fly.
* **ACID Compliance:** Uses **Delta Lake** technology to ensure data integrity during concurrent read/write operations.
* **Live Dashboarding:** Integrated with Power BI via DirectQuery for up-to-the-second visualization.

---

## 🏗 Architecture
The pipeline follows a modern **Medallion Architecture** (Bronze/Silver layers) optimized for streaming data.

```mermaid
graph LR
    A[Python Producer] -->|JSON Stream| B(Azure Event Hubs)
    B -->|Kafka Protocol| C{Azure Databricks}
    subgraph Spark Cluster
    C -->|Extract| D[Read Stream]
    D -->|Transform| E[NLP Analysis]
    E -->|Load| F[(Delta Lake Table)]
    end
    F -->|DirectQuery| G[Power BI Dashboard]


### Data Flow
1. **Source:** A local Python script generates synthetic e-commerce reviews using the `Faker` library.
2. **Ingestion:** Data is pushed to **Azure Event Hubs**, acting as a decoupled message buffer.
3. **Processing:** **Azure Databricks** (Apache Spark) reads the stream, parses the JSON, and applies a UDF (User Defined Function) to determine if the review is Positive, Negative, or Neutral.
4. **Storage:** The enriched data is persisted into a **Delta Table**, ensuring a reliable serving layer.
5. **Serving:** **Power BI** queries the Delta Table in real-time to visualize trends.

## 🛠 Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.9, PySpark | Core logic and scripting. |
| **Cloud Provider** | Microsoft Azure | Infrastructure hosting. |
| **Ingestion** | Azure Event Hubs | Kafka-compatible event streaming platform. |
| **Processing** | Apache Spark 3.5.0 | Distributed data processing engine on Azure Databricks. |
| **NLP** | TextBlob | Library for processing textual data. |
| **Storage** | Delta Lake | Open-source storage layer that brings reliability to data lakes. |
| **Visualization** | Power BI | Business analytics service for interactive visualizations. |

## 📋 Prerequisites
Before running this project, ensure you have:
* **Microsoft Azure Subscription** (Free Tier/Student is sufficient).
* **Power BI Desktop** (Windows) for visualization.
* **Python 3.x** installed locally.
* **Azure Databricks Workspace** (Standard Tier).

## ⚙ Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/Azure-Sentiment-Pipeline.git](https://github.com/YOUR_USERNAME/Azure-Sentiment-Pipeline.git)
cd Azure-Sentiment-Pipeline


###2. Install Dependencies
pip install -r requirements.txt
3. Azure Resource Configuration
Event Hubs: Create a Namespace (Standard Tier) and an Event Hub named user_reviews.

Databricks: Deploy a workspace in a supported region (e.g., Southeast Asia or East US).

Cluster: Create a Compute Cluster with Runtime 14.3 LTS (Scala 2.12, Spark 3.5.0).

4. Configure the Producer
Open producer.py and update the connection string:

Python

# producer.py
CONNECTION_STR = "Endpoint=sb://<YOUR_NAMESPACE>.servicebus.windows.net/;SharedAccessKeyName=..."
EVENT_HUB_NAME = "user_reviews"
5. Deploy Spark Job
Import spark_processor_cloud.py into your Databricks Workspace.

Install the textblob library on your cluster (%pip install textblob).

Add your Event Hub connection string to the notebook configuration.

🚀 Usage Guide
Step 1: Start the Data Stream
Run the producer script locally to start generating mock data:

Bash

python producer.py
Output: [2025-12-16 10:00:01] Sent: {'user_id': 45, 'review': 'Great product!', ...}

Step 2: Run the Cloud Processor
Execute the Databricks notebook. It will initialize the stream and begin populating the sentiment_live_data Delta table.

Step 3: Monitor in Power BI
Open Power BI Desktop.

Select Get Data > Azure Databricks.

Connect using DirectQuery mode.

Select the sentiment_live_data table.

Click Refresh to see the latest sentiment scores updating live.

🧠 Key Engineering Challenges
1. Region Quota Limitations
Problem: The Azure Student subscription had a 0-core quota for VM types in the UAE North region, preventing cluster creation.

Solution: Migrated infrastructure to the Southeast Asia region, where Standard_DS3_v2 quotas were available for student tiers.

2. Kafka/Spark Dependency Conflicts
Problem: Databricks uses a shaded version of Kafka libraries. Standard org.apache.kafka login modules caused ClassNotFoundException.

Solution: Utilized the kafkashaded namespace in the Spark configuration:

Python

"kafka.sasl.jaas.config": 'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule...'
3. Real-Time Visualization Latency
Problem: Standard Power BI Import mode only refreshes 8 times a day.

Solution: Implemented DirectQuery combined with Delta Lake, allowing the dashboard to query the storage layer directly without data duplication, achieving near real-time updates.

📂 Project Structure
Plaintext

Azure-Sentiment-Pipeline/
├── producer.py                 # Local script to generate & stream data
├── spark_processor_cloud.py    # PySpark logic for Databricks
├── spark_processor_local.py    # Local testing version (optional)
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
🔮 Future Improvements
[ ] Dockerize Producer: Containerize the Python script for deployment on Azure Kubernetes Service (AKS).

[ ] Advanced AI: Replace TextBlob with a Transformer-based model (e.g., BERT) for higher accuracy.

[ ] Alerting System: Integrate Azure Logic Apps to send email alerts when negative sentiment spikes > 50%.

👤 Author
[Mohammed Showharwade Neshad]

[https://www.linkedin.com/in/mohammed-showharwade-n-082628101/]

[https://github.com/SwNishad]