import os
import boto3
import pymysql  # For MySQL RDS
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def lambda_handler(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    if bucket != 'cardiovascular-disease-data':
        print(f"Unexpected bucket: {bucket}")
        return

    s3_client = boto3.client('s3')
    local_file_path = '/tmp/' + os.path.basename(key)
    s3_client.download_file(bucket, key, local_file_path)

    cleaned_data = clean_data(pd.read_csv(local_file_path))

    # Retrieve database connection details
    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    db_connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = db_connection.cursor()

    with pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name) as db_connection:
        with db_connection.cursor() as cursor:
            # Insert cleaned data into the MySQL table
            cursor.execute("""
                INSERT INTO cardio-db (age, gender, height, weight, ap_hi, ap_lo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (cleaned_data['age'], cleaned_data['gender'], cleaned_data['height'],
                  cleaned_data['weight'], cleaned_data['ap_hi'], cleaned_data['ap_lo']))

    db_connection.commit()

    print("Data inserted successfully.")

def clean_data(data):
    data = data.dropna()

    data = data.drop_duplicates()

    data['age'] = data['age'] // 365  
    data['height'] = pd.to_numeric(data['height'], errors='coerce')
    data['weight'] = pd.to_numeric(data['weight'], errors='coerce')

    data['gender'] = data['gender'].map({1: 'Female', 2: 'Male'})
    data['cholesterol'] = data['cholesterol'].map({1: 'Normal', 2: 'Above normal', 3: 'Well above normal'})
    data['gluc'] = data['gluc'].map({1: 'Normal', 2: 'Above normal', 3: 'well above normal'})

    return data

