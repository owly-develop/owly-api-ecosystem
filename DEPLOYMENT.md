# AWS Deployment Guide

Complete guide for deploying OWLY CRM API to AWS.

## Prerequisites

- AWS Account
- AWS CLI installed and configured
- Docker installed locally
- Domain name (optional but recommended)

## Architecture Overview

```
┌─────────────────┐
│   CloudFront    │ (Optional CDN)
└────────┬────────┘
         │
┌────────▼────────┐
│  Load Balancer  │
└────────┬────────┘
         │
┌────────▼────────┐
│   ECS Fargate   │ (Django API)
│   Auto Scaling  │
└────────┬────────┘
         │
    ┌────▼─────┬──────────┬──────────┐
    │          │          │          │
┌───▼───┐ ┌───▼───┐ ┌───▼────┐ ┌──▼───┐
│  RDS  │ │ Redis │ │   S3   │ │ SES  │
│ (PG)  │ │(Cache)│ │(Media) │ │(Email)│
└───────┘ └───────┘ └────────┘ └──────┘
```

## Step 1: Setup RDS PostgreSQL

### 1.1 Create Database
```bash
aws rds create-db-instance \
    --db-instance-identifier owly-crm-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 16.1 \
    --master-username owlyuser \
    --master-user-password <your-secure-password> \
    --allocated-storage 20 \
    --vpc-security-group-ids <your-security-group> \
    --db-subnet-group-name <your-subnet-group> \
    --backup-retention-period 7 \
    --storage-encrypted \
    --publicly-accessible false
```

### 1.2 Note Connection Details
```
Host: owly-crm-db.<region>.rds.amazonaws.com
Port: 5432
Database: postgres
Username: owlyuser
Password: <your-password>
```

## Step 2: Setup ElastiCache Redis

### 2.1 Create Redis Cluster
```bash
aws elasticache create-cache-cluster \
    --cache-cluster-id owly-crm-redis \
    --cache-node-type cache.t3.micro \
    --engine redis \
    --engine-version 7.0 \
    --num-cache-nodes 1 \
    --cache-subnet-group-name <your-subnet-group> \
    --security-group-ids <your-security-group>
```

### 2.2 Note Connection Details
```
Host: owly-crm-redis.<region>.cache.amazonaws.com
Port: 6379
```

## Step 3: Setup S3 Bucket

### 3.1 Create Bucket
```bash
aws s3 mb s3://owly-crm-media
```

### 3.2 Configure CORS
Create `cors.json`:
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

Apply:
```bash
aws s3api put-bucket-cors \
    --bucket owly-crm-media \
    --cors-configuration file://cors.json
```

### 3.3 Create IAM User for S3
```bash
aws iam create-user --user-name owly-s3-user
aws iam attach-user-policy \
    --user-name owly-s3-user \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

aws iam create-access-key --user-name owly-s3-user
```

## Step 4: Build and Push Docker Image

### 4.1 Create ECR Repository
```bash
aws ecr create-repository --repository-name owly-crm-api
```

### 4.2 Login to ECR
```bash
aws ecr get-login-password --region <region> | \
docker login --username AWS --password-stdin \
<account-id>.dkr.ecr.<region>.amazonaws.com
```

### 4.3 Build and Push
```bash
docker build -t owly-crm-api .

docker tag owly-crm-api:latest \
<account-id>.dkr.ecr.<region>.amazonaws.com/owly-crm-api:latest

docker push \
<account-id>.dkr.ecr.<region>.amazonaws.com/owly-crm-api:latest
```

## Step 5: Setup ECS Cluster

### 5.1 Create Cluster
```bash
aws ecs create-cluster --cluster-name owly-crm-cluster
```

### 5.2 Create Task Definition
Create `task-definition.json`:
```json
{
  "family": "owly-crm-api",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "web",
      "image": "<account-id>.dkr.ecr.<region>.amazonaws.com/owly-crm-api:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DEBUG",
          "value": "False"
        },
        {
          "name": "USE_S3",
          "value": "True"
        }
      ],
      "secrets": [
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:<region>:<account>:secret:owly/SECRET_KEY"
        },
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:<region>:<account>:secret:owly/DATABASE_URL"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/owly-crm-api",
          "awslogs-region": "<region>",
          "awslogs-stream-prefix": "web"
        }
      }
    }
  ]
}
```

Register:
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

### 5.3 Create Service with Load Balancer
```bash
aws ecs create-service \
    --cluster owly-crm-cluster \
    --service-name owly-crm-service \
    --task-definition owly-crm-api \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[<subnet-ids>],securityGroups=[<sg-id>],assignPublicIp=ENABLED}" \
    --load-balancers "targetGroupArn=<target-group-arn>,containerName=web,containerPort=8000"
```

## Step 6: Setup Secrets Manager

### 6.1 Store Secrets
```bash
# Secret Key
aws secretsmanager create-secret \
    --name owly/SECRET_KEY \
    --secret-string "<your-secret-key>"

# Database URL
aws secretsmanager create-secret \
    --name owly/DATABASE_URL \
    --secret-string "postgresql://owlyuser:<pass>@<rds-host>:5432/postgres"

# AWS S3 Credentials
aws secretsmanager create-secret \
    --name owly/AWS_ACCESS_KEY_ID \
    --secret-string "<your-access-key>"

aws secretsmanager create-secret \
    --name owly/AWS_SECRET_ACCESS_KEY \
    --secret-string "<your-secret-key>"
```

## Step 7: Run Database Migrations

### 7.1 Connect to ECS Task
```bash
# Get task ID
TASK_ID=$(aws ecs list-tasks \
    --cluster owly-crm-cluster \
    --service-name owly-crm-service \
    --query 'taskArns[0]' --output text)

# Execute migration
aws ecs execute-command \
    --cluster owly-crm-cluster \
    --task $TASK_ID \
    --container web \
    --interactive \
    --command "python manage.py migrate"
```

### 7.2 Create Superuser
```bash
aws ecs execute-command \
    --cluster owly-crm-cluster \
    --task $TASK_ID \
    --container web \
    --interactive \
    --command "python manage.py createsuperuser"
```

## Step 8: Setup Domain and SSL

### 8.1 Request Certificate
```bash
aws acm request-certificate \
    --domain-name api.owlycrm.com \
    --validation-method DNS
```

### 8.2 Configure Load Balancer
Add HTTPS listener on port 443 with the certificate.

### 8.3 Update DNS
Point `api.owlycrm.com` to the Load Balancer DNS name.

## Step 9: Setup Auto Scaling

### 9.1 Create Scaling Policy
```bash
aws application-autoscaling register-scalable-target \
    --service-namespace ecs \
    --scalable-dimension ecs:service:DesiredCount \
    --resource-id service/owly-crm-cluster/owly-crm-service \
    --min-capacity 2 \
    --max-capacity 10

aws application-autoscaling put-scaling-policy \
    --policy-name cpu-scaling-policy \
    --service-namespace ecs \
    --scalable-dimension ecs:service:DesiredCount \
    --resource-id service/owly-crm-cluster/owly-crm-service \
    --policy-type TargetTrackingScaling \
    --target-tracking-scaling-policy-configuration \
    '{"TargetValue":70.0,"PredefinedMetricSpecification":{"PredefinedMetricType":"ECSServiceAverageCPUUtilization"}}'
```

## Step 10: Setup Celery Workers

### 10.1 Create Celery Task Definition
Similar to web task but with command:
```json
"command": ["celery", "-A", "owly_crm", "worker", "-l", "info"]
```

### 10.2 Create Celery Beat Task Definition
```json
"command": ["celery", "-A", "owly_crm", "beat", "-l", "info"]
```

### 10.3 Create Services
```bash
aws ecs create-service \
    --cluster owly-crm-cluster \
    --service-name owly-crm-celery \
    --task-definition owly-crm-celery \
    --desired-count 1 \
    --launch-type FARGATE

aws ecs create-service \
    --cluster owly-crm-cluster \
    --service-name owly-crm-celery-beat \
    --task-definition owly-crm-celery-beat \
    --desired-count 1 \
    --launch-type FARGATE
```

## Monitoring

### CloudWatch Logs
```bash
aws logs tail /ecs/owly-crm-api --follow
```

### Health Check
```bash
curl https://api.owlycrm.com/api/health/
```

## Cost Estimation

- **RDS (t3.micro)**: ~$15/month
- **ElastiCache (t3.micro)**: ~$12/month
- **ECS Fargate (2 tasks)**: ~$30/month
- **Load Balancer**: ~$16/month
- **S3**: ~$1-5/month (depends on usage)
- **Data Transfer**: Variable

**Total**: ~$75-100/month

## Backup Strategy

### RDS Automated Backups
- Enabled by default (7 days retention)
- Manual snapshots before major updates

### S3 Versioning
```bash
aws s3api put-bucket-versioning \
    --bucket owly-crm-media \
    --versioning-configuration Status=Enabled
```

## Rollback Procedure

### Rollback to Previous Task Definition
```bash
aws ecs update-service \
    --cluster owly-crm-cluster \
    --service owly-crm-service \
    --task-definition owly-crm-api:<previous-revision>
```

## Troubleshooting

### Check Service Status
```bash
aws ecs describe-services \
    --cluster owly-crm-cluster \
    --services owly-crm-service
```

### View Logs
```bash
aws logs get-log-events \
    --log-group-name /ecs/owly-crm-api \
    --log-stream-name <stream-name>
```

### Connect to Task
```bash
aws ecs execute-command \
    --cluster owly-crm-cluster \
    --task <task-id> \
    --container web \
    --interactive \
    --command "/bin/bash"
```

---

**Deployment Complete! 🚀**

Your OWLY CRM API is now running on AWS with:
- High availability (multi-AZ)
- Auto-scaling
- Load balancing
- Managed database
- Redis caching
- S3 media storage
- SSL/TLS encryption

