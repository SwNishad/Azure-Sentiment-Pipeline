## ☁️ Real-Time Sentiment Analysis Pipeline on Azure

![Status](https://img.shields.io/badge/Status-Completed-success)
![Azure](https://img.shields.io/badge/Azure-Event%20Hubs%20|%20Databricks-blue)
![Spark](https://img.shields.io/badge/Apache%20Spark-Structured%20Streaming-orange)
![PowerBI](https://img.shields.io/badge/Visualization-Power%20BI-yellow)


## 📌 Project Overview
In the age of high-frequency social media and e-commerce, businesses cannot afford to wait for daily batch jobs to understand customer sentiment. This project implements a **Real-Time Data Engineering Pipeline** that ingests, processes, and visualizes simulated user reviews instantly.
## 🎥 Demo
[https://drive.google.com/file/d/1M3-WkyacVNCoK-_PhCQFo8FX8yk7Xyqp/view?usp=sharing]

**Goal:** Transform raw, unstructured text streams into actionable business intelligence with sub-second latency.

**Key Features:**
* **High-Throughput Ingestion:** Capable of handling thousands of events per second via Azure Event Hubs.
* **Real-Time NLP:** Uses Spark Structured Streaming and Python's `TextBlob` to calculate sentiment polarity on the fly.
* **ACID Compliance:** Uses **Delta Lake** technology to ensure data integrity during concurrent read/write operations.
* **Live Dashboarding:** Integrated with Power BI via DirectQuery for up-to-the-second visualization.

---

## 🏗 Architecture
<img width="614" height="1019" alt="image" src="https://github.com/user-attachments/assets/93cf8e49-a73e-4568-9229-c8fb9f24b642" />




### Data Flow
1. **Source:** A local Python script generates synthetic e-commerce reviews using the `Faker` library.
2. **Ingestion:** Data is pushed to **Azure Event Hubs**, acting as a decoupled message buffer.
3. **Processing:** **Azure Databricks** (Apache Spark) reads the stream, parses the JSON, and applies a UDF (User Defined Function) to determine if the review is Positive, Negative, or Neutral.
4. **Storage:** The enriched data is persisted into a **Delta Table**, ensuring a reliable serving layer.
5. **Serving:** **Power BI** queries the Delta Table in real-time to visualize trends.

## 🛠 Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.9, PySpark | Core logic and scripting |
| **Cloud Provider** | Microsoft Azure | Infrastructure hosting |
| **Ingestion** | Azure Event Hubs | Kafka-compatible event streaming platform |
| **Processing** | Apache Spark 3.5.0 | Distributed data processing engine on Azure Databricks |
| **NLP** | TextBlob | Library for processing textual data |
| **Storage** | Delta Lake | Open-source storage layer that brings reliability to data lakes |
| **Visualization** | Power BI | Business analytics service for interactive visualizations |

## 📋 Prerequisites
Before running this project, ensure you have:
* **Microsoft Azure Subscription** (Free Tier/Student is sufficient).
* **Power BI Desktop** (Windows) for visualization.
* **Python 3.x** installed locally.
* **Azure Databricks Workspace** (Standard Tier).

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Azure-Sentiment-Pipeline.git
cd Azure-Sentiment-Pipeline
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Azure Resource Configuration

#### 🔹 Event Hubs
- Create an **Event Hubs Namespace** (Standard Tier)
- Create an Event Hub named:
  ```text
  user_reviews
  ```

#### 🔹 Azure Databricks
- Deploy a Databricks workspace in a supported region:
  - **Southeast Asia** or **East US** (recommended for student subscriptions)

#### 🔹 Databricks Cluster
- Runtime: **14.3 LTS**
- Spark Version: **3.5.0**
- Scala: **2.12**

---

### 4️⃣ Configure the Producer

Open `producer.py` and update the Event Hub connection details:

```python
# producer.py
CONNECTION_STR = "Endpoint=sb://<YOUR_NAMESPACE>.servicebus.windows.net/;SharedAccessKeyName=..."
EVENT_HUB_NAME = "user_reviews"
```

---

### 5️⃣ Deploy the Spark Job

1. Import `spark_processor_cloud.py` into your **Databricks Workspace**
2. Install required library on the cluster:

```python
%pip install textblob
```

3. Add the Event Hub connection string to the Spark configuration inside the notebook

---

## 🚀 Usage Guide

### ▶️ Step 1: Start the Data Stream

Run the producer locally to generate mock user reviews:

```bash
python producer.py
```

**Sample Output:**
```text
[2025-12-16 10:00:01] Sent: {'user_id': 45, 'review': 'Great product!', ...}
```

---

### ▶️ Step 2: Run the Cloud Processor

- Execute the Databricks notebook
- Spark initializes a streaming job
- Processed data is written into:

```text
sentiment_live_data (Delta Table)
```

---

### ▶️ Step 3: Monitor in Power BI

1. Open **Power BI Desktop**
2. Select **Get Data → Azure Databricks**
3. Connect using **DirectQuery** mode
4. Select the `sentiment_live_data` table
5. Click **Refresh** to see live sentiment updates

---

## 🧠 Key Engineering Challenges

### 1️⃣ Region Quota Limitations

**Problem**  
Azure Student subscription had **0-core VM quota** in the **UAE North** region, blocking cluster creation.

**Solution**  
Migrated all infrastructure to **Southeast Asia**, where `Standard_DS3_v2` quotas were available for student tiers.

---

### 2️⃣ Kafka / Spark Dependency Conflicts

**Problem**  
Databricks uses shaded Kafka libraries, causing `ClassNotFoundException` with standard Kafka login modules.

**Solution**  
Used the shaded Kafka namespace in Spark configuration:

```python
"kafka.sasl.jaas.config": 'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule ...'
```

---

### 3️⃣ Real-Time Visualization Latency

**Problem**  
Power BI Import mode refreshes only **8 times/day**.

**Solution**  
Implemented **DirectQuery + Delta Lake**, allowing Power BI to query Databricks storage directly, enabling **near real-time dashboards**.

---

## 📂 Project Structure

```text
Azure-Sentiment-Pipeline/
├── producer.py                 # Local script to generate & stream data
├── spark_processor_cloud.py    # PySpark logic for Databricks
├── spark_processor_local.py    # Local testing version (optional)
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

---

## 🔮 Future Improvements

- [ ] **Dockerize Producer** – Containerize the producer and deploy on **Azure Kubernetes Service (AKS)**
- [ ] **Advanced AI Models** – Replace TextBlob with Transformer-based models (BERT, RoBERTa)
- [ ] **Alerting System** – Integrate **Azure Logic Apps** to trigger alerts when negative sentiment exceeds 50%

---

## 👤 Author

**Mohammed Showharwade Neshad**  

- 🔗 LinkedIn: https://www.linkedin.com/in/mohammed-showharwade-n-082628101/  
- 💻 GitHub: https://github.com/SwNishad

---

⭐ *If this project helped you, consider giving it a star!*

