# create_bucket_upload.py

import boto3
import uuid

def main():
    session = boto3.Session(region_name="us-east-1")  # change region if needed
    s3 = session.resource("s3")

    # Unique bucket name (must be globally unique)
    unique_id = str(uuid.uuid4())[:8]
    bucket_name = f"boto3-demo-bucket-{unique_id}"

    print(f"Creating bucket: {bucket_name}")
    bucket = s3.Bucket(bucket_name)

    # Some regions require LocationConstraint; us-east-1 can omit it
    bucket.create()

    # Create a simple test file content
    object_key = "test-file.txt"
    content = "Hello from Boto3 script for the cloud blog project!\n"

    print(f"Uploading object: s3://{bucket_name}/{object_key}")
    obj = bucket.Object(object_key)
    obj.put(Body=content.encode("utf-8"))

    print("Done.")
    print(f"You can verify in S3 console: bucket = {bucket_name}, key = {object_key}")

if __name__ == "__main__":
    main()
