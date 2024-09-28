import os
import json
import boto3
import hashlib
import time
import requests
from flask import Flask, request, jsonify
from botocore.exceptions import ClientError
from dotenv import load_dotenv

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# AWS configurations
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
KNOWLEDGE_BASE_ID = os.getenv('KNOWLEDGE_BASE_ID')
DATA_SOURCE_ID= os.getenv('DATA_SOURCE_ID')
BEDROCK_MODEL_ID = os.getenv('BEDROCK_MODEL_ID')
TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1000'))

# Pinata configurations
PINATA_API_KEY = os.getenv('PINATA_API_KEY')
PINATA_SECRET_API_KEY = os.getenv('PINATA_SECRET_API_KEY')
PINATA_JWT = os.getenv('PINATA_JWT')

# Initialize AWS clients using environment variables
s3_client = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

bedrock_runtime = boto3.client('bedrock-runtime',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

bedrock = boto3.client('bedrock-agent',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

def fetch_files_from_pinata():
    """Fetch files from Pinata and return their content."""
    url = "https://api.pinata.cloud/data/pinList?status=pinned"
    headers = {
        "Authorization": f"Bearer {PINATA_JWT}"
    }
    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()
    
    files = []
    for item in response.json()['rows']:
        file_url = f"https://gateway.pinata.cloud/ipfs/{item['ipfs_pin_hash']}"
        file_content = requests.get(file_url, verify=False).text
        files.append({
            'name': item['metadata']['name'],
            'content': file_content
        })
    return files

def sync_files_with_s3():
    """Sync Pinata files with S3 bucket."""
    files = fetch_files_from_pinata()
    for file in files:
        file_content = file['content'].encode('utf-8')
        file_md5 = hashlib.md5(file_content).hexdigest()

        try:
            # Check if file exists in S3 and compare MD5
            s3_object = s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=file['name'])
            s3_md5 = s3_object['ETag'].strip('"')

            if file_md5 != s3_md5:
                print(f"Updating {file['name']} in S3...")
                s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=file['name'], Body=file_content)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                # File doesn't exist in S3, upload it
                print(f"Uploading new file {file['name']} to S3...")
                s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=file['name'], Body=file_content)
            else:
                print(f"Error checking {file['name']} in S3: {e}")

def sync_knowledge_base():
    """Sync AWS Bedrock knowledge base."""
    try:
        response = bedrock.start_ingestion_job(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            dataSourceId=DATA_SOURCE_ID,
        )
        job_id = response['ingestionJob']['ingestionJobId']
        print(f"Knowledge base sync started. Job ID: {job_id}")

        # Wait for the ingestion job to complete
        while True:
            try:
                job_status = bedrock.get_ingestion_job(
                    dataSourceId=DATA_SOURCE_ID,
                    knowledgeBaseId=KNOWLEDGE_BASE_ID,
                    ingestionJobId=job_id
                )['ingestionJob']['status']
                
                if job_status == 'COMPLETE':
                    print("Knowledge base sync completed successfully.")
                    break
                elif job_status in ['FAILED', 'STOPPED']:
                    print(f"Knowledge base sync {job_status}.")
                    break
                else:
                    print(f"Knowledge base sync in progress. Status: {job_status}")
                    time.sleep(5) 
            except ClientError as e:
                print(f"Error checking ingestion job status: {e}")
                break

    except ClientError as e:
        print(f"Error starting ingestion job: {e}")
    except Exception as e:
        print(f"Unexpected error syncing knowledge base: {e}")

#  Sync files and knowledge base before starting the server
sync_files_with_s3()
sync_knowledge_base()

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    
    try:
        # First, retrieve relevant information from the knowledge base
        retrieve_response = bedrock.retrieve(
            knowledgeBaseId=KNOWLEDGE_BASE_ID,
            retrievalQuery={
                'text': user_message
            },
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': 3
                }
            }
        )

        # Extract the retrieved passages
        retrieved_passages = [result['content'] for result in retrieve_response['retrievalResults']]
        
        # Construct the prompt with retrieved information
        context = "\n".join(retrieved_passages)
        prompt = f"Based on the following information:\n\n{context}\n\nAnswer the question: {user_message}\n\nOnly use the information provided above to answer the question. If the information is not sufficient to answer the question, say so."

        # Prepare the request body for Bedrock
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        # Call Bedrock API for model inference
        response = bedrock_runtime.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(request_body)
        )

        # Parse the response
        response_body = json.loads(response['body'].read())
        ai_response = response_body['content'][0]['text']

        # Extract sources from the retrieved results
        sources = [result['location']['s3Location']['uri'] for result in retrieve_response['retrievalResults']]

        return jsonify({
            'response': ai_response,
            'sources': sources
        })

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({
            'error': 'An error occurred while processing your request.'
        }), 500

if __name__ == '__main__':
    app.run(debug=False)
