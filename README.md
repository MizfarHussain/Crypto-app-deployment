Simple Scalable Crypto Price API
This is a lightweight web application built with Python and Flask that serves cryptocurrency prices from the CoinGecko API. It is designed to be containerized with Docker and deployed on scalable cloud infrastructure like AWS Elastic Container Service (ECS).

This project includes:

app.py: The main Flask application with two endpoints:

/: Fetches and returns the current price of Bitcoin, Ethereum, and Ripple.

/health: A simple health check endpoint.

requirements.txt: A list of Python dependencies.

Dockerfile: Instructions to build a Docker image for the application.

buildspec.yml: Build instructions for AWS CodeBuild, used for CI/CD.

How to Run Locally
1. Without Docker (Using a Virtual Environment)
First, create and activate a virtual environment:

# Create a virtual environment
python3 -m venv venv

# Activate it (on macOS/Linux)
source venv/bin/activate

# On Windows
# venv\Scripts\activate

Next, install the dependencies and run the app:

# Install dependencies
pip install -r requirements.txt

# Run the Flask development server
flask --app app run

The application will be running at http://127.0.0.1:5000.

2. With Docker
Ensure you have Docker installed and running on your machine.

# 1. Build the Docker image
# The -t flag tags the image with a name (e.g., crypto-app)
docker build -t crypto-app .

# 2. Run the Docker container from the image
# The -p flag maps port 8000 of the container to port 8000 on your machine
docker run -p 8000:8000 crypto-app

The application will be accessible at http://localhost:8000.

High-Level AWS Deployment Guide (ECR & ECS)
This application is ready to be deployed on a scalable infrastructure. Here is a summary of the steps to deploy it on AWS.

Step 1: Push the Docker Image to ECR (Elastic Container Registry)
ECR is a private Docker registry where you can store your container images.

Create an ECR Repository: Go to the ECR service in the AWS Console and create a new private repository (e.g., my-crypto-app).

Authenticate Docker: Select your new repository and click "View push commands". Follow the instructions to log your Docker client into your AWS account.

Tag Your Image: Tag your local Docker image with the ECR repository URI.

docker tag crypto-app:latest YOUR_AWS_ACCOUNT_ID.dkr.ecr.YOUR_[REGION.amazonaws.com/my-crypto-app:latest](https://REGION.amazonaws.com/my-crypto-app:latest)

Push the Image: Push the tagged image to your ECR repository.

docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.YOUR_[REGION.amazonaws.com/my-crypto-app:latest](https://REGION.amazonaws.com/my-crypto-app:latest)

Step 2: Deploy the Image with ECS (Elastic Container Service)
ECS runs and manages your Docker containers.

Create an ECS Cluster: A cluster is a logical grouping of tasks or services. You can start with a simple "Networking only" (Fargate) cluster.

Create a Task Definition:

A Task Definition is a blueprint for your application.

Select Fargate as the launch type.

In the "Container definitions" section, click "Add container".

Container name: crypto-app-container

Image: Paste the ECR image URI from the previous step.

Port mappings: Configure it to expose port 8000, which is the port our gunicorn server is running on.

Create an ECS Service:

A Service ensures that a specified number of instances of your task definition are running and maintained.

Go to your cluster and create a new Service.

Select your Task Definition.

Number of tasks: Start with 1 or 2. ECS will automatically scale this up or down based on your configuration.

Networking: Choose your VPC and subnets. Ensure you have a security group that allows inbound traffic on port 8000.

Load Balancing (Optional but Recommended): You can create an Application Load Balancer (ALB) that distributes traffic across your tasks. The ALB's target group should use the /health endpoint for health checks.

Once the service is running, ECS will pull your image from ECR and run it. If you configured a load balancer, you can access your application using the load balancer's DNS name.

CI/CD with AWS CodePipeline and CodeBuild
To automate the deployment process, you can set up a CI/CD pipeline using AWS services. The included buildspec.yml file is used by AWS CodeBuild to define the build process.

buildspec.yml: This file contains a series of commands for building the Docker image, pushing it to ECR, and preparing an artifact for ECS deployment.

AWS CodeCommit/GitHub: Store your source code in a Git repository. This will be the source stage for your pipeline.

AWS CodePipeline: Create a new pipeline.

Source Stage: Connect it to your repository (e.g., the main branch).

Build Stage:

Create a new CodeBuild project.

Point it to your source code.

CodeBuild will automatically detect and use the buildspec.yml file.

Important: You must give the CodeBuild service role permissions to interact with ECR (e.g., ecr:GetAuthorizationToken, ecr:BatchCheckLayerAvailability, ecr:InitiateLayerUpload, ecr:UploadLayerPart, ecr:CompleteLayerUpload, ecr:PutImage).

Deploy Stage:

Choose Amazon ECS as the deployment provider.

Select your ECS cluster and service.

The Image definitions file will be the output artifact from the build stage (imagedefinitions.json).

When you push new code to your repository, CodePipeline will automatically trigger, build the new Docker image, push it to ECR, and update your ECS service to deploy the new version.
