# invoke_lambda.py

import boto3
import json

def main():
    session = boto3.Session(region_name="us-east-1")  # adjust if needed
    lambda_client = session.client("lambda")

    # Replace with your actual Lambda function name
    function_name = "cloud-blog-s3-upload-logger"

    payload = {
        "source": "manual-boto3-test",
        "message": "Hello from Boto3 invoke!"
    }

    print(f"Invoking Lambda function: {function_name}")
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",  # wait for response
        Payload=json.dumps(payload).encode("utf-8")
    )

    print("StatusCode:", response.get("StatusCode"))
    resp_payload = response["Payload"].read().decode("utf-8")
    print("Lambda response payload:", resp_payload)

if __name__ == "__main__":
    main()
