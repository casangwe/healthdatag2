from check import check_bucket_exists, check_file_exists, upload_file
from config import bucket_name, cardio

def main():
    # Check if the S3 bucket exists
    if not check_bucket_exists(bucket_name):
        print(f"Bucket '{bucket_name}' does not exist.")
        return
    
    # Check if the file already exists in the bucket
    if check_file_exists(bucket_name, cardio):
        print(f"File '{cardio}' already exists in the bucket.")
    else:
        # Upload the file if it doesn't exist
        result = upload_file(cardio, bucket_name)
        if result:
            print("Upload successful!")
        else:
            print("Upload failed.")

if __name__ == "__main__":
    main()
