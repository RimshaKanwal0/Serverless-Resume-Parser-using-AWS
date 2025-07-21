import json
import boto3
import uuid
import datetime
import re

# AWS clients
textract = boto3.client('textract')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# Environment settings
TABLE_NAME = 'ResumeData'
TOPIC_ARN = 'arn:aws:sns:ap-south-1:688930149975:ResumeNotificationTopic'

def extract_name(text):
    """Try to extract name from the beginning of the resume"""
    lines = text.split('\n')
    for line in lines:
        if line.strip() and len(line.strip().split()) <= 3 and not re.search(r'\d', line):
            return line.strip().title()
    return "N/A"

def extract_skills(text):
    """Extract skills using simple keyword heuristics"""
    skills_section = re.findall(r'(Skill[s]? Highlights|Technical Skills|Skills)[\s\S]{0,300}', text, re.IGNORECASE)
    if skills_section:
        section_text = skills_section[0]
        skills = re.findall(r'\b[A-Za-z\+\#]{2,}\b', section_text)
        return list(set(skills))
    return []

def lambda_handler(event, context):
    print("🚀 Lambda triggered!")
    print("🔍 Event:", json.dumps(event))

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        print(f"📄 File received: {key} from bucket: {bucket}")
        print("📑 Calling Textract...")

        # Call Textract
        response = textract.detect_document_text(
            Document={'S3Object': {'Bucket': bucket, 'Name': key}}
        )

        blocks = response.get('Blocks', [])
        lines = [block['Text'] for block in blocks if block['BlockType'] == 'LINE']
        full_text = '\n'.join(lines)

        print("✅ Textract completed.")
        print("📝 Extracted Text:")
        print(full_text)

        # Save raw Textract text as JSON file in S3
        textract_json_key = key.replace('uploads/', 'processed/').replace('.pdf', '_textract.json')
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket=bucket,
            Key=textract_json_key,
            Body=json.dumps(response)
        )
        print(f"📁 Textract JSON saved at: {textract_json_key}")

        # Extract email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', full_text)
        email = email_match.group(0) if email_match else "Not found"

        # Extract name and skills
        name = extract_name(full_text)
        skills = extract_skills(full_text)

        print("👤 Name:", name)
        print("📧 Email:", email)
        print("🛠️ Skills:", skills)

        # Save to DynamoDB
        print("📦 Saving to DynamoDB...")
        table = dynamodb.Table(TABLE_NAME)
        item = {
            'id': str(uuid.uuid4()),
            'file_name': key,
            'name': name,
            'email': email,
            'skills': skills,
            'timestamp': str(datetime.datetime.utcnow())
        }
        table.put_item(Item=item)
        print("✅ Saved to DynamoDB")

        # Send SNS notification
        message = f"Resume processed:\nName: {name}\nEmail: {email}\nFile: {key}"
        try:
            sns.publish(
                TopicArn=TOPIC_ARN,
                Message=message,
                Subject='✅ Resume Parsed Notification'
            )
            print("📨 SNS Email Sent")
        except Exception as e:
            print(f"❌ SNS Publish Error: {str(e)}")

    return {
        'statusCode': 200,
        'body': json.dumps('Resume processing complete!')
    }
