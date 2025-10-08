# 🎓 Campus Help Assistant – AWS-Powered Chatbot System

An intelligent, serverless chatbot built using **Amazon Lex**, **AWS Lambda**, and **DynamoDB** that helps university students and staff register complaints, get FAQs, and access campus-related information in real-time.

---

## 🚀 Overview

This project demonstrates how to build a **fully serverless chatbot system** using AWS services.  
It consists of:
- **Amazon Lex** – Conversational interface for natural language understanding  
- **AWS Lambda (Python)** – Executes business logic  
- **Amazon DynamoDB** – Stores chat logs and complaint data  
- **S3 (Frontend Hosting)** – Hosts the chatbot web interface  
- **Cognito** – Provides secure guest authentication  
- **CloudWatch** – Monitors logs and chatbot performance  

---

## 🧠 Features

✅ Register and track complaints (stored in DynamoDB)  
✅ Real-time text-based conversation using AWS Lex  
✅ Secure API execution via Lambda  
✅ Web-based chatbot interface (HTML, Tailwind, JavaScript)  
✅ Serverless – no backend servers required  
✅ Scalable, lightweight, and deployable in any AWS region  

---

## 🗂️ Project Structure

Campus_Help_Assistant_AWS/
│
├── index.html # Frontend UI
├── style.css # Custom CSS (minor overrides)
├── script.js # Lex + AWS JS SDK integration
│
├── lambda_function.py # AWS Lambda backend logic
├── requirements.txt # Python dependencies for Lambda
│
└── README.md # Project documentation

markdown
Copy code

---

## ⚙️ Setup Instructions

### 1. 🧩 Prerequisites

You’ll need:
- An AWS account
- IAM user with admin privileges
- Basic understanding of AWS Lex, Lambda, and DynamoDB

### 2. 🗨️ Create an Amazon Lex Bot

1. Go to the **AWS Lex Console**
2. Create a new bot (English, Version 2)
3. Add sample intents, e.g.:
   - `RegisterComplaint`
   - `GetFAQ`
   - `Greetings`
4. Connect each intent to a Lambda function (will be created next)

---

### 3. ⚙️ Create Lambda Function

1. Go to **AWS Lambda → Create Function**
2. Runtime: `Python 3.9`
3. Paste the content of `lambda_function.py`
4. Create a **DynamoDB Table**:
   - Name: `CampusComplaints`
   - Primary key: `complaint_id` (String)
5. Add environment variable in Lambda:
DYNAMO_TABLE=CampusComplaints

markdown
Copy code
6. Attach `AmazonDynamoDBFullAccess` and `AWSLambdaBasicExecutionRole` policies.

---

### 4. 🪣 Host the Frontend

1. Create an **S3 bucket** (example: `campus-help-assistant`)
2. Enable **Static website hosting**
3. Upload:
- `index.html`
- `style.css`
- `script.js`
4. In `script.js`, replace placeholders:
```js
AWS.config.region = "ap-south-1"; // or your region
IdentityPoolId: "YOUR_COGNITO_POOL_ID";
botId: "YOUR_LEX_BOT_ID";
botAliasId: "YOUR_BOT_ALIAS_ID";
5. 🔍 Test Your Chatbot
Open the S3 website URL.

Start chatting!

View complaint entries in DynamoDB and monitor logs in CloudWatch.
