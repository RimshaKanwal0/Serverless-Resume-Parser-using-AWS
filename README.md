# Serverless-Resume-Parser-using-AWS

A fully serverless application that automates resume parsing, storage, analysis, and notification workflows using AWS services.

This project allows users to upload resumes via a static website. The resumes are processed using AWS Lambda and Amazon Textract, saved as JSON in S3, indexed into DynamoDB, and queried using Amazon Athena. Users are notified via Amazon SNS.

---

## 🔧 Tech Stack

| Service          | Description                                              |
|------------------|----------------------------------------------------------|
| **Amazon S3**     | Stores uploaded resumes and Textract JSON output        |
| **Amazon Textract** | Extracts text from PDF resumes                          |
| **AWS Lambda**     | Orchestrates parsing logic and data flow                |
| **Amazon DynamoDB**| Stores structured key resume fields (name, email, etc.)|
| **Amazon SNS**     | Sends email notification after parsing completes       |
| **Amazon Athena**  | Allows querying JSON files stored in S3                |
| **Amazon CloudWatch** | Logs function execution and metrics                    |

---

## 🧱 Architecture

![Architecture Diagram](architecture.png)

---

## ⚙️ Workflow

1. **User Uploads** a resume via a static website or directly to S3 (`uploads/` folder).
2. **Amazon S3** triggers **AWS Lambda**.
3. **Lambda**:
   - Calls **Amazon Textract** to extract text.
   - Saves raw output as JSON to S3 (`processed/` folder).
   - Parses key details (name, email, skills).
   - Saves structured data to **DynamoDB** (`ResumeData` table).
   - Sends email via **SNS**.
4. **Amazon Athena**:
   - Enables running SQL-like queries over JSON stored in S3 (`processed/*.json`).
5. **CloudWatch**:
   - Logs execution for debugging and auditing.

---

## 🧪 Sample Athena Query

To query the extracted data in S3 via Athena, ensure:
- You’ve created a table with `jsonserde` or Glue crawler
- Your JSON files are stored under a single prefix like `processed/`
etc
**Save them in a File/sql**

**📸 Screenshots
Add screenshots of:**

-Static website upload

-S3 file structure

-DynamoDB items

-CloudWatch logs

-Athena query result
etc

**Save them in a folder: screenshots/**
<img width="1920" height="1009" alt="upload_page" src="https://github.com/user-attachments/assets/000c229c-7131-4f6a-b4a7-de1ee90a60ed" />
<img width="1920" height="981" alt="s3_uploads1" src="https://github.com/user-attachments/assets/4adaf809-b923-4e10-b7f0-f76b7a880aa2" />
<img width="1920" height="972" alt="dynamodb_table" src="https://github.com/user-attachments/assets/49342191-96ae-442c-a751-50743844746c" />
<img width="1920" height="975" alt="cloudwatch_logs" src="https://github.com/user-attachments/assets/12e29c66-0cd8-4cbe-931b-7423d1ca30fa" />



**🙋‍♀️ Author**
Rimsha Kanwal
Email: Rimshakanwal7110.com
[GitHub:](https://github.com/RimshaKanwal0) 
