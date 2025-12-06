# Cloud Blog Platform on AWS

A scalable, cloud-native blog platform built on Amazon Web Services (AWS) demonstrating Infrastructure-as-Code (IaC), serverless architecture, and modern DevOps practices.

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Terraform](https://img.shields.io/badge/terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white)
![CloudFormation](https://img.shields.io/badge/CloudFormation-FF4F00?style=for-the-badge&logo=amazon-aws&logoColor=white)
![PHP](https://img.shields.io/badge/php-%23777BB4.svg?style=for-the-badge&logo=php&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Component Details](#component-details)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Deployment Guide](#deployment-guide)
- [Web Application](#web-application)
- [API Integration](#api-integration)
- [Boto3 Scripts](#boto3-scripts)
- [Data Flow](#data-flow)
- [Challenges & Solutions](#challenges--solutions)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## 🎯 Overview

This project demonstrates the design and deployment of a production-ready, scalable web application using AWS cloud services. The platform allows users to create blog posts with images, categorize content, apply tags, and view posts through an elegant web interface.

**Key Highlights:**
- Infrastructure provisioned using **Terraform** and **AWS CloudFormation**
- Serverless image processing with **AWS Lambda**
- Auto-scaling web servers behind an **Application Load Balancer**
- Secure image storage in **Amazon S3**
- MySQL database hosted on **Amazon RDS**
- Real-time API integration with **API Gateway**
- Programmatic AWS interaction via **Boto3 SDK**

## 🏗️ Architecture

┌─────────────────────────────────────────────────────────────┐
│                         Internet                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Application Load    │
              │      Balancer        │
              │   (Internet-facing)  │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Auto Scaling Group │
              │   (Min:1, Max:2)     │
              └──────────┬───────────┘
                         │
                         ▼
                    ┌────────┐
                    │  EC2   │
                    │ (PHP)  │
                    │ Apache │
                    └────┬───┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐   ┌─────────┐   ┌──────────────┐
    │   RDS   │   │   S3    │   │ API Gateway  │
    │ (MySQL) │   │ Bucket  │   │   + Lambda   │
    └─────────┘   └────┬────┘   └──────────────┘
                       │
                       ▼
                 ┌──────────┐        ┌──────────┐
                 │  Lambda  │───────▶│CloudWatch│
                 │ (S3 Log) │        │   Logs   │
                 └──────────┘        └──────────┘
```

### AWS Services Used

| Service | Purpose |
|---------|---------|
| **EC2** | Web application hosting (Apache + PHP) |
| **RDS (MySQL)** | Relational database for blog metadata |
| **S3** | Image storage |
| **Lambda** | Serverless image upload logging |
| **API Gateway** | RESTful API endpoint |
| **ALB** | Load balancing and high availability |
| **Auto Scaling** | Dynamic capacity management |
| **CloudWatch** | Monitoring and logging |
| **IAM** | Access management and security |
| **VPC** | Network isolation |

## 🔧 Component Details

### 1. Networking (VPC)

| Component | Configuration |
|-----------|--------------|
| **VPC CIDR** | 10.0.0.0/16 |
| **Public Subnets** | 10.0.1.0/24, 10.0.2.0/24 |
| **Private Subnets** | 10.0.10.0/24, 10.0.20.0/24 |
| **Availability Zones** | us-east-1a, us-east-1b |
| **Internet Gateway** | Enabled for public internet access |
| **NAT Gateway** | Used to allow outbound internet access from private subnets |

> **Provisioned using:** Terraform

### 2. Compute (EC2)

| Component | Configuration |
|-----------|--------------|
| **Instance Type** | t3.micro |
| **Operating System** | Amazon Linux 2 |
| **Auto Scaling Group** | Min: 1, Max: 2, Desired: 1 |
| **Scaling Behavior** | Automatic instance replacement via ASG |
| **Placement** | Public subnets, behind Application Load Balancer |
| **Application Stack** | Apache + PHP serving dynamic blog application |

> **Deployed using:** CloudFormation

### 3. Load Balancing (ALB)

| Component | Configuration |
|-----------|--------------|
| **Type** | Application Load Balancer |
| **Scheme** | Internet-facing |
| **Listeners** | HTTP (Port 80) |
| **Target Type** | EC2 Instances |
| **Health Checks** | Root path (`/`) |
| **DNS Access** | Public ALB DNS endpoint |

> **Deployed using:** CloudFormation

### 4. Database (Amazon RDS)

| Component | Configuration |
|-----------|--------------|
| **Engine** | MySQL |
| **Instance Class** | db.t3.micro |
| **Storage** | General Purpose (20 GB) |
| **Multi-AZ** | Disabled (development setup) |
| **Network Placement** | Private subnets |
| **Public Access** | Disabled |
| **Encryption** | Enabled |

**Database Schema Stores:**
- Blog posts
- Categories
- Tags
- Image references

> **Deployed using:** CloudFormation

### 5. Storage (Amazon S3)

| Component | Configuration |
|-----------|--------------|
| **Bucket Purpose** | Blog image uploads |
| **Access** | Private |
| **Encryption** | AES-256 server-side encryption |
| **Public Access** | Blocked |
| **Access Method** | IAM role via EC2 application |
| **Delivery to Users** | Images proxied via PHP (`image.php`) for secure access |

> **Provisioned using:** CloudFormation

### 6. Serverless (AWS Lambda)

#### 🔹 S3 Upload Logger Lambda

| Component | Configuration |
|-----------|--------------|
| **Runtime** | Python 3.x |
| **Memory** | 128 MB |
| **Timeout** | 30 seconds |
| **Trigger** | S3 ObjectCreated events |
| **Function Purpose** | Logs each image upload |
| **Output** | Amazon CloudWatch Logs |

#### 🔹 API Gateway Lambda (Bonus Feature)

| Component | Configuration |
|-----------|--------------|
| **Runtime** | Python 3.x |
| **Trigger** | HTTP invocations via API Gateway |
| **Route** | `GET /info` |
| **Purpose** | Returns project status JSON (timestamp, environment, region) |
| **Integration** | Called from homepage via JavaScript |

### 7. API Gateway (Bonus Integration)

| Component | Configuration |
|-----------|--------------|
| **API Type** | HTTP API |
| **Route** | `/info` |
| **Integration** | Lambda proxy |
| **CORS** | Enabled |
| **Invocation Source** | Homepage Fetch API call |
| **Output** | Real-time JSON rendered in UI |

**Purpose:** Demonstrates HTTP-based serverless invocation independent of ALB/EC2.

### 8. Security Architecture

#### Security Groups

| Group | Rules |
|-------|-------|
| **ALB Security Group** | Inbound: HTTP (80) from `0.0.0.0/0`<br>Outbound: All |
| **EC2 Security Group** | Inbound: HTTP (80) from ALB SG, SSH (22) from admin IP only<br>Outbound: All |
| **RDS Security Group** | Inbound: MySQL (3306) from EC2 SG only |

> Security groups were managed via CloudFormation to centralize service access control.

## ✨ Features

### Blog Functionality
- ✅ Create blog posts with rich content
- ✅ Upload and display images
- ✅ Categorize posts
- ✅ Tag system for content organization
- ✅ Featured posts section
- ✅ Search functionality
- ✅ Category filtering
- ✅ Responsive, modern UI design

### Cloud Features
- ✅ Auto-scaling for high availability
- ✅ Load balancing across multiple instances
- ✅ Serverless image processing
- ✅ Automated CloudWatch logging
- ✅ Real-time API status display
- ✅ Infrastructure as Code (IaC)
- ✅ Secure database in private subnets

## 🛠️ Technologies Used

### Infrastructure as Code
- **Terraform** - VPC, subnets, networking, routing, NAT Gateway
- **AWS CloudFormation** - ALB, Auto Scaling, EC2, RDS, S3, Lambda, security groups

### Application Stack
- **PHP 7.4+** - Backend application logic
- **Apache** - Web server
- **MySQL** - Database (via Amazon RDS)
- **HTML/CSS/JavaScript** - Frontend interface

### AWS SDK & CLI
- **Boto3 (Python)** - Programmatic AWS interactions
- **AWS CLI** - Command-line management and resource inspection

### Additional Tools
- **Composer** - PHP dependency management
- **AWS SDK for PHP** - S3 integration

## 📁 Project Structure

```
project/
├── boto3_scripts/              # Python scripts for AWS automation
│   ├── create_bucket_upload.py
│   ├── get_instance_metadata.py
│   ├── invoke_lambda.py
│   └── list_running_instances.py
│
├── cloudformation/             # CloudFormation templates
│   └── appf2-stack.yaml       # Application stack template
│
├── terraform/                  # Terraform configuration
│   ├── main.tf                # Main Terraform configuration
│   ├── variables.tf           # Variable definitions
│   ├── outputs.tf             # Output values
│   └── terraform.tfvars       # Variable values
│
├── Web Application Files (on EC2)
│   ├── index.php              # Homepage
│   ├── create_post.php        # Post creation page
│   ├── post.php               # Individual post view
│   ├── image.php              # Image proxy script
│   ├── config.php             # Configuration file
│   ├── db.php                 # Database connection
│   ├── composer.json          # PHP dependencies
│   └── composer.lock          # Dependency lock file
│
└── README.md                   # This file
```

## 📋 Prerequisites

### AWS Account Setup
- Active AWS account
- AWS CLI configured with appropriate credentials
- IAM user with administrator access (for deployment)

### Local Development Tools
- Terraform >= 1.0
- AWS CLI >= 2.0
- Python 3.8+
- Boto3 library (`pip install boto3`)

### AWS Resources Required
- VPC with public and private subnets
- EC2 key pair for SSH access
- S3 bucket for image storage
- RDS MySQL database

## 🚀 Deployment Guide

### Step 1: Deploy Networking Infrastructure (Terraform)

```bash
cd terraform/

# Initialize Terraform
terraform init

# Review the execution plan
terraform plan

# Apply the configuration
terraform apply -auto-approve

# Note the output values (VPC ID, Subnet IDs)
terraform output
```

**Terraform Outputs:**
- VPC ID
- Public Subnet IDs
- Private Subnet IDs

### Step 2: Deploy Application Stack (CloudFormation)

```bash
cd ../cloudformation/

# Deploy the CloudFormation stack
aws cloudformation create-stack \
  --stack-name cloud-blog-app \
  --template-body file://appf2-stack.yaml \
  --parameters \
    ParameterKey=VpcId,ParameterValue=<VPC_ID_FROM_TERRAFORM> \
    ParameterKey=PublicSubnet1,ParameterValue=<SUBNET_1_ID> \
    ParameterKey=PublicSubnet2,ParameterValue=<SUBNET_2_ID> \
    ParameterKey=PrivateSubnet1,ParameterValue=<PRIVATE_SUBNET_1_ID> \
    ParameterKey=PrivateSubnet2,ParameterValue=<PRIVATE_SUBNET_2_ID> \
  --capabilities CAPABILITY_IAM

# Monitor stack creation
aws cloudformation describe-stacks \
  --stack-name cloud-blog-app \
  --query 'Stacks[0].StackStatus'

# Get ALB DNS name
aws cloudformation describe-stacks \
  --stack-name cloud-blog-app \
  --query 'Stacks[0].Outputs[?OutputKey==`LoadBalancerDNS`].OutputValue' \
  --output text
```

### Step 3: Configure Web Application

1. **SSH into EC2 instance:**
```bash
ssh -i your-key.pem ec2-user@<EC2_PUBLIC_IP>
```

2. **Install dependencies:**
```bash
# Install Apache and PHP
sudo yum update -y
sudo yum install -y httpd php php-mysqlnd php-xml

# Install Composer
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer

# Install AWS SDK for PHP
cd /var/www/html
composer require aws/aws-sdk-php
```

3. **Upload application files:**
```bash
# From your local machine
scp -i your-key.pem -r *.php ec2-user@<EC2_PUBLIC_IP>:/var/www/html/
```

4. **Configure database connection:**
Edit `config.php` with your RDS endpoint:
```php
$db_host = 'your-rds-endpoint.rds.amazonaws.com';
$db_user = 'admin';
$db_pass = 'your-password';
$db_name = 'blog_db';
$s3_bucket = 'your-bucket-name';
$aws_region = 'us-east-1';
```

5. **Set up database schema:**
```bash
mysql -h <RDS_ENDPOINT> -u admin -p blog_db < schema.sql
```

### Step 4: Verify Deployment

1. Access the blog via ALB DNS: `http://<ALB-DNS-NAME>`
2. Create a test blog post with an image
3. Verify image upload in S3 console
4. Check CloudWatch logs for Lambda execution
5. Verify API status section displays live data

## 🌐 Web Application

### Homepage (`index.php`)
- Displays all blog posts with pagination
- Featured posts section
- Category filter dropdown
- Search functionality
- API status display (live data from API Gateway)
- Category cards for quick filtering

### Create Post Page (`create_post.php`)
- Form-based post creation
- Image upload to S3
- Category selection
- Tag input (comma-separated)
- Featured post toggle
- Success/error messaging

### Post Detail Page (`post.php`)
- Full post content display
- Image rendering from S3
- Category and tags display
- Timestamp information

### Design Features
- Modern gradient background
- Warm color scheme (browns and creams)
- Responsive layout
- Smooth hover animations
- Inter font family
- Card-based UI components

## 🔌 API Integration

### API Gateway + Lambda Architecture

**Endpoint:** `https://qfwoay04l0.execute-api.us-east-1.amazonaws.com/info`

**Response Format:**
```json
{
  "message": "Cloud Blog API is running",
  "projectName": "Cloud Blog Platform",
  "environment": "production",
  "region": "us-east-1",
  "timestamp": "2024-12-06T10:30:45Z"
}
```

**Frontend Integration:**
The homepage uses JavaScript Fetch API to retrieve and display live API data:
```javascript
fetch(apiUrl)
  .then(response => response.json())
  .then(data => {
    // Display API status dynamically
  });
```

## 🐍 Boto3 Scripts

### 1. Create S3 Bucket and Upload File
**File:** `boto3_scripts/create_bucket_upload.py`

Creates a uniquely named S3 bucket and uploads a test file.

```bash
python boto3_scripts/create_bucket_upload.py
```

### 2. Get EC2 Instance Metadata
**File:** `boto3_scripts/get_instance_metadata.py`

Retrieves metadata from the running EC2 instance (must run from EC2).

```bash
python boto3_scripts/get_instance_metadata.py
```

**Output:**
- Instance ID
- AMI ID
- Instance Type
- Availability Zone

### 3. List Running EC2 Instances
**File:** `boto3_scripts/list_running_instances.py`

Lists all running EC2 instances in the region.

```bash
python boto3_scripts/list_running_instances.py
```

### 4. Invoke Lambda Function
**File:** `boto3_scripts/invoke_lambda.py`

Invokes a Lambda function with a test payload.

```bash
python boto3_scripts/invoke_lambda.py
```

## 🔄 Data Flow

### User Request Flow
```
User Browser → Internet Gateway → ALB → EC2 (PHP App) → RDS
```

### File Upload Flow
```
User Upload → EC2 → S3 → S3 Event → Lambda → CloudWatch Logs
```

### API Gateway Flow
```
Browser → API Gateway (/info) → Lambda → JSON → UI status panel
```

### Auto Scaling Flow
```
CloudWatch Monitoring → Auto Scaling Group → EC2 Launch/Terminate
```

## 💰 Cost Optimization

- Small instance sizes (`t3.micro`, `db.t3.micro`)
- Single NAT Gateway (development setup)
- RDS Single-AZ deployment
- Auto Scaling to avoid excess capacity
- Serverless logging only invoked on-demand

## 🔧 Challenges & Solutions

### 1. Auto Scaling Instance Replacement
**Challenge:** Manual configuration changes were lost when Auto Scaling Group replaced instances.

**Solution:** Suspended health-replacement actions during configuration steps. Implemented proper AMI baking process for production deployments.

### 2. IAM Permission Errors
**Challenge:** Initial S3 uploads failed due to missing IAM permissions.

**Solution:** Updated EC2 instance IAM role policies to include `s3:PutObject` and `s3:GetObject` permissions for the designated bucket.

### 3. Route Misconfiguration
**Challenge:** Editing inactive EC2 instances caused application version mismatches.

**Solution:** Always ensured SSH access to the current target group instance serving traffic. Implemented proper deployment procedures.

### 4. Database Connectivity
**Challenge:** EC2 instances couldn't connect to RDS in private subnets.

**Solution:** Verified security group rules allowed MySQL port 3306 from EC2 security group. Ensured proper subnet routing.

## 🚀 Future Enhancements

- [ ] Add HTTPS using AWS ACM certificates
- [ ] Integrate CloudFront CDN for faster asset delivery
- [ ] Introduce REST APIs for CRUD operations
- [ ] Enable Multi-AZ RDS failover for production
- [ ] Implement CI/CD pipelines with GitHub Actions and CodeDeploy
- [ ] Deploy WAF for ALB protection
- [ ] Add full pagination and advanced tag filtering to UI
- [ ] Add user authentication with Amazon Cognito
- [ ] Create comprehensive CloudWatch dashboards
- [ ] Implement automated backups with AWS Backup
- [ ] Add ElastiCache for database query caching
- [ ] Implement blue-green deployment strategy
- [ ] Integrate Amazon SES for email notifications
- [ ] Implement image optimization with Lambda

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Abhinav Alarayil**
- GitHub: [@abhinav-2105](https://github.com/abhinav-2105)
- LinkedIn: [Abhinav Alarayil](https://www.linkedin.com/in/abhinav-alarayil-b7a5a5234/)

## 🙏 Acknowledgments

- AWS Documentation
- Terraform Registry
- CloudFormation User Guide
- AWS Well-Architected Framework

---

**⭐ If you found this project helpful, please consider giving it a star!**

## 📞 Support

For questions or issues, please open an issue in the GitHub repository.

---

**Last Updated:** December 2025