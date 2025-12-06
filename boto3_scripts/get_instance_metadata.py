import urllib.request

def get_metadata(path):
    # First retrieve the session token
    token_req = urllib.request.Request(
        "http://169.254.169.254/latest/api/token",
        method="PUT",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
    )
    token = urllib.request.urlopen(token_req).read().decode()

    # Then use the token to get metadata
    req = urllib.request.Request(
        f"http://169.254.169.254/latest/meta-data/{path}",
        headers={"X-aws-ec2-metadata-token": token}
    )
    return urllib.request.urlopen(req).read().decode()

if __name__ == "__main__":
    try:
        instance_id = get_metadata("instance-id")
        ami_id = get_metadata("ami-id")
        instance_type = get_metadata("instance-type")

        print("Instance ID:", instance_id)
        print("AMI ID:", ami_id)
        print("Instance Type:", instance_type)

    except Exception as e:
        print("Failed to retrieve instance metadata:", e)
