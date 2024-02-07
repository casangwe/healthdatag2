Healthcare Data Analysis

The purpose of our product is to establish a streamlined data pipeline in a cloud environment, addressing challenges in data management and analysis. By integrating amazon S3 buckets, Lambda functions, RDS, and potentially EC2.

Cardiovascular Disease:
https://www.kaggle.com/datasets/sulianova/cardiovascular-disease-dataset

User docs:
1 - Clone GitHub repository onto local machine
2 - Create a '.gitignore' file in your directory
3 - Create a 'config.py' file in your directory and add this file name into the '.gitignore' file you created in the previous step.
3a. Copy the code below and paste it in the 'config.py' file. Make sure to replace the values with the actual values found in you AWS configuration

        config.py:

        # AWS S3 configuration

        aws_access_key_id = 'replace_with_your_access_key'
        aws_secret_access_key = 'replace_with_your_secret_access_key'
        region_name = 'replace_with_desired_region'
        bucket_name = 'replace_with_bucket_name'

        # RDS configuration

        rds_endpoint = 'replace_with_rds_endpoint'
        rds_port = ####
        rds_username = 'insert_rds_username'
        rds_password = '********'
        # rds_database = ''

        # Constants

        cardio = 'cardio_train.csv'

4 - Install the required imports found at the header of each script (boto, mysql.connector, etc)
