import os
import boto3
import pymysql  # For MySQL RDS
import pandas as pd

def lambda_handler(event):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    s3_client = boto3.client('s3')
    local_file_path = '/tmp/' + os.path.basename(key)
    s3_client.download_file(bucket, key, local_file_path)

    cleaned_data = clean_data(local_file_path)

    db_connection = pymysql.connect(host='cardio-db.crkc44qquibr.us-east-1.rds.amazonaws.com',
                                   user='admin',
                                   password='rootroot',
                                   database='cardio-db')
    cursor = db_connection.cursor()

    cursor.execute("INSERT INTO your_table (column1, column2) VALUES (%s, %s)", (cleaned_data['col1'], cleaned_data['col2']))

    db_connection.commit()
    db_connection.close()


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

lambda_handler(event):

