# SDN DDoS Detection using AWS Lambda and Machine Learning

This project integrates Software Defined Networking (SDN) with Machine Learning (ML) and Serverless Computing to detect DDoS (Distributed Denial-of-Service) attacks in real-time. It utilizes a POX controller to monitor network traffic, which is then analyzed by a machine learning model deployed using AWS Lambda and Docker.

---

## 🚀 Project Overview

- **SDN Controller:** POX with a custom `flow_monitor_aws.py` script to capture flow statistics.
- **ML Model:** Random Forest classifier trained to detect normal and DDoS traffic.
- **Deployment:** Model containerized using Docker, stored in AWS ECR, and deployed via AWS Lambda.
- **Frontend Trigger:** Mininet topology simulating traffic (normal and DDoS).
- **Backend API:** AWS Lambda URL which responds with predictions in real-time.

---

## 🛠️ Project Structure

```

sdn-ddos-aws/
│
├── venv/ # Python virtual environment
├── pox/ # POX controller directory
│ └── flow_monitor_aws.py # Custom controller script
├── rf_model.pkl # Trained Random Forest model
├── scaler.pkl # Feature scaler for normalization
├── app.py # Lambda handler function
├── requirements.txt # Python dependencies
├── Dockerfile # For containerizing the ML model
└── topo.py # Mininet custom topology

```

---

## 🧠 Machine Learning Model

We experimented with various ML models and chose **Random Forest** due to its:

- High accuracy: **98.64%**
- Fast predictions
- Lightweight nature

### Models Tested

| Model               | Accuracy   | Time Taken  |
| ------------------- | ---------- | ----------- |
| Logistic Regression | 75.23%     | ~0.7 sec    |
| SVM (RBF Kernel)    | 91.77%     | ~1140 sec   |
| KNN (k=1)           | 97.28%     | ~28 sec     |
| **Random Forest**   | **98.64%** | **~30 sec** |

---

## 🐳 Containerization

To deploy the model on AWS Lambda, we containerized it using Docker.
Files used:

- `rf_model.pkl` and `scaler.pkl`: Generated during model training using `pickle`
- `app.py`: Lambda function that handles input and returns predictions
- `requirements.txt`: Ensure the versions match the local training environment
- `Dockerfile`: Defines how to build the image

---

## ☁️ AWS ECR and Lambda Deployment

### Push to AWS ECR

1. **Configure AWS CLI:**

```bash
aws configure
```

2. **Login to ECR:**

```bash
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com
```

3. **Tag & Push the Image:**

```bash
docker build -t sdn-ml-image .
docker tag sdn-ml-image:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/sdn-ml-image
docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/sdn-ml-image
```

---

### Link with AWS Lambda

1. Search for **Lambda** in AWS Console.
2. Click on **Create function** > **Container image**.
3. Set function name (e.g., `ddosAlert2`) and paste your ECR image URL.
4. Configure:

   - Memory: `1024 MB`
   - Timeout: `2 minutes`

5. Assign a role with permission to access ECR and execute Lambda.
6. After deployment, enable Function URL and configure CORS.

---

## 🧪 Testing

### Start POX Controller:

```bash
cd sdn-ddos-aws
source venv/bin/activate
cd pox
sudo ./pox.py log.level --DEBUG forwarding.l2_learning flow_monitor_aws
```

### Start Mininet:

```bash
cd sdn-ddos-aws
sudo python3 topo.py
```

### Test Traffic

- **Normal Traffic (Prediction: 0)**

```bash
h1 ping -c 5 h2
```

- **DDoS Simulation (Prediction: 1)**

```bash
h1 nping --tcp -p 80 --flags SYN --rate 1000 -c 5000 10.0.0.2
```

---

## 📈 Results

| Traffic Type | Example Command   | Prediction |
| ------------ | ----------------- | ---------- |
| Normal       | `ping`            | 0          |
| DDoS Attack  | `nping --tcp ...` | 1          |

---

## ✅ Conclusion

This project demonstrates an end-to-end DDoS detection pipeline using SDN and ML in a serverless cloud environment. The use of AWS Lambda and Docker provides scalability and flexibility. With accurate predictions and real-time response, this system shows how intelligent traffic monitoring can be effectively implemented in software-defined networks.

---

## 📸 Architecture Diagram

![Architecture Diagram](https://github.com/deveshanurag/serverless-computing-sdn-/blob/main/architecutre.png)

---

## Authors

- **Devesh Kumar**  
  _Computer Science and Engineering, PDPM IIITDM Jabalpur_
- **Ankit Singh**  
  _Computer Science and Engineering, PDPM IIITDM Jabalpur_
- **Sudhanshu**  
  _Computer Science and Engineering, PDPM IIITDM Jabalpur_

## Acknowledgments

This research received support during the **BTP** project, instructed by **Professor Munesh Singh**, at **PDPM IIITDM Jabalpur**.
