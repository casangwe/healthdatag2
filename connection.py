import boto3
import mysql.connector
from config import aws_access_key_id, aws_secret_access_key, region_name, bucket_name, \
    rds_endpoint, rds_port, rds_username, rds_password, rds_database

def connect_to_s3():
    try:
        s3 = boto3.client('s3', 
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          region_name=region_name)
        print("Connected to S3 successfully.")
        return s3
    except Exception as e:
        print("An error occurred while connecting to S3:", e)
        return None

def connect_to_rds():
    try:
        connection = mysql.connector.connect(
            host=rds_endpoint,
            port=rds_port,
            user=rds_username,
            password=rds_password,
        )
        print("Connected to RDS successfully.")
        return connection
    
    except Exception as e:
        print("An error occurred while connecting to RDS:", e)
        return None

if __name__ == "__main__":
    s3_connection = connect_to_s3()
    rds_connection = connect_to_rds()
