# list_running_instances.py

import boto3

def main():
    session = boto3.Session(region_name="us-east-1")  # adjust region
    ec2 = session.client("ec2")

    response = ec2.describe_instances(
        Filters=[
            {"Name": "instance-state-name", "Values": ["running"]}
        ]
    )

    print("Running EC2 instances:\n")

    found_any = False
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            instance_id = instance.get("InstanceId")
            instance_type = instance.get("InstanceType")
            state = instance.get("State", {}).get("Name")
            az = instance.get("Placement", {}).get("AvailabilityZone")

            print(f"- ID: {instance_id}")
            print(f"  Type: {instance_type}")
            print(f"  AZ:   {az}")
            print(f"  State:{state}")
            print()

            found_any = True

    if not found_any:
        print("No running instances found in this region.")

if __name__ == "__main__":
    main()
