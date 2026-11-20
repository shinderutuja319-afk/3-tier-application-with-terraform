# CloudTask – AWS 3-Tier Application Deployment with Terraform

CloudTask is a containerized task management application built using a three-tier application architecture and deployed on AWS infrastructure provisioned with Terraform.

The project demonstrates Infrastructure as Code (IaC), containerization, cloud infrastructure provisioning, application deployment, and secure instance management.

## Architecture

CloudTask consists of three application layers:

1. **Presentation Layer:** HTML, CSS, JavaScript, and Nginx.
2. **Application Layer:** Python Flask REST API served using Gunicorn.
3. **Database Layer:** PostgreSQL for persistent task storage.

All three application layers run as Docker containers on a single Amazon EC2 instance using Docker Compose.

### AWS Infrastructure

- Amazon VPC
- Public Subnet
- Internet Gateway
- Route Table
- Security Group
- Amazon EC2 (t3.micro)
- IAM Role and Instance Profile
- AWS Systems Manager (SSM) access

### Architecture Diagram

```text
                 Internet
                    |
                    |
              Internet Gateway
                    |
                    |
               Public Subnet
                    |
                    |
               Security Group
                    |
                    |
              Amazon EC2
              (Amazon Linux)
                    |
              Docker Compose
                    |
          +---------+----------+
          |                    |
      Frontend              Backend
       Nginx                Flask API
          |                    |
          |                    |
          +--------+-----------+
                   |
                PostgreSQL
                 Database
```

**Note:** This is a cost-conscious portfolio implementation. The three application tiers are separated into Docker services, but they currently share one EC2 instance. This is not a highly available or production-grade multi-subnet deployment.

## Technologies Used

| Category | Technologies |
|---|---|
| Cloud Platform | AWS |
| Infrastructure as Code | Terraform |
| Compute | Amazon EC2 |
| Networking | VPC, Subnet, Internet Gateway, Route Table |
| Security | IAM, Security Groups, AWS Systems Manager |
| Containerization | Docker |
| Container Orchestration | Docker Compose |
| Frontend | HTML, CSS, JavaScript, Nginx |
| Backend | Python, Flask, Gunicorn |
| Database | PostgreSQL |
| Version Control | Git, GitHub |

## Project Structure

```text
aws-3tier-app-deployment/
│
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── nginx.conf
│
├── backend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
│
├── database/
│   └── schema.sql
│
├── terraform/
│   ├── provider.tf
│   ├── version.tf
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars
│   │
│   └── modules/
│       ├── vpc/
│       ├── security-groups/
│       ├── ec2/
│       ├── iam/
│       ├── rds/
│       ├── alb/
│       ├── ecr/
│       ├── autoscaling/
│       └── monitoring/
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

*Some module directories are reserved for possible future extensions and are not part of the current deployment.*

## Application Features

- Create new tasks.
- View all tasks.
- Mark tasks as completed.
- Update task information.
- Delete tasks.
- Store task data in PostgreSQL.
- Persistent database storage using Docker volumes.
- Nginx reverse proxy for backend API requests.
- Containerized frontend, backend, and database services.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Check backend health |
| GET | `/api/tasks` | Retrieve all tasks |
| POST | `/api/tasks` | Create a task |
| PATCH | `/api/tasks/<id>` | Update a task |
| DELETE | `/api/tasks/<id>` | Delete a task |

## Local Setup

### Prerequisites

- Git
- Docker Desktop
- Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/shinderutuja319-afk/3-tier-application-with-terraform.git
```

```bash
cd 3-tier-application-with-terraform
```

### 2. Start the application

```bash
docker compose up -d --build
```

### 3. Check running containers

```bash
docker compose ps
```

### 4. Access the application

Open your browser:

```text
http://localhost:8080
```

### 5. Stop the application

```bash
docker compose down
```

To remove the local database volume as well (this permanently deletes its stored data):

```bash
docker compose down -v
```

## AWS Infrastructure Setup

Terraform is used to provision AWS infrastructure.

### Prerequisites

- AWS account
- AWS CLI
- Terraform
- Configured AWS credentials

### 1. Configure AWS CLI

```bash
aws configure
```

Set the AWS region to:

```text
ap-south-1
```

### 2. Navigate to Terraform directory

```bash
cd terraform
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Format Terraform files

```bash
terraform fmt -recursive
```

### 5. Validate configuration

```bash
terraform validate
```

### 6. Review infrastructure changes

```bash
terraform plan
```

Review the plan and estimated AWS costs before proceeding.

**Important:** Only create AWS resources after reviewing the plan and confirming the expected costs. Running `terraform plan` does not provision infrastructure.

## Security Considerations

- EC2 instance access is designed around AWS Systems Manager (SSM), avoiding the need to expose SSH port 22.
- IAM roles provide permissions to the EC2 instance.
- Security Groups control inbound and outbound traffic.
- PostgreSQL is not directly exposed to the internet.
- Terraform state files and environment secrets must not be committed to GitHub.
- Database credentials should be supplied securely and never hardcoded into production configuration.

## Future Improvements

Possible future enhancements include:

- Separate public and private subnets.
- Application Load Balancer.
- Amazon RDS for managed database hosting.
- Auto Scaling.
- Amazon ECR for container image storage.
- GitHub Actions CI/CD pipeline.
- Kubernetes deployment.
- HTTPS using TLS certificates.
- CloudWatch monitoring and logging.

These enhancements are not included in the current cost-conscious deployment.

## Learning Outcomes

Through this project, I am developing practical experience with:

- AWS infrastructure provisioning using Terraform.
- VPC networking and subnet configuration.
- IAM roles and instance profiles.
- Secure EC2 access using AWS Systems Manager.
- Docker image creation and container management.
- Docker Compose networking and persistent volumes.
- Deploying a Flask application with PostgreSQL.
- Git and GitHub version control.

## Author

**Rutuja Shinde**

MCA Graduate | Aspiring AWS Cloud / DevOps Engineer

GitHub: https://github.com/shinderutuja319-afk

---

*This project is developed as a hands-on cloud and DevOps learning project, with an emphasis on Infrastructure as Code, containerization, AWS fundamentals, and cost-conscious cloud deployment.*