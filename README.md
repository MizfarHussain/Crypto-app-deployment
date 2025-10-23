# Simple & Scalable Crypto Price API
A lightweight web application built with Python and Flask that serves cryptocurrency prices from the CoinGecko API. It is designed to be containerized with Docker and deployed on a scalable AWS infrastructure using ECS and ECR, complete with a CI/CD pipeline via CodeBuild.

✨ Features
 1. API Endpoint: Get real-time prices for Bitcoin, Ethereum, and Ripple.
 2. Health Check: /health endpoint for load balancer health checks.
 3.Containerized: Ready to be deployed as a Docker container.
 4. Scalable: Designed for scalable cloud services like AWS ECS.
 5. Automated: Includes a buildspec.yml for CI/CD with AWS CodeBuild.

🚀 Getting Started
 Prerequisites
 Python 3.9+
 
 Docker Desktop
 
 Local Development
 First, create and activate a virtual environment to manage dependencies.
 
 Create a virtual environment:
 
  For macOS/Linux
 python3 -m venv venv
 
  For Windows
 python -m venv venv
 
 
 Activate the environment:
 
  For macOS/Linux
 source venv/bin/activate
 
  For Windows
 - .\venv\Scripts\activate
 - Install dependencies and run the app:  
 - Install required packages  
 - pip install -r requirements.txt  
 - Run the Flask development server  
 - flask --app app run  
 - The application will be running at http://127.0.0.1:5000.  
 - Running with Docker  
 - Build the Docker image:  
 - The -t flag tags the image with a name (e.g., crypto-app)  
 - docker build -t crypto-app .  
 - Run the Docker container:  
 - The -p flag maps port 8000 of the container to port 8000 on your machine  
 - docker run -p 8000:8000 crypto-app  
 - The application will be accessible at http://localhost:8000.  

# ☁️ AWS Deployment Guide
This application is ready for a scalable cloud deployment.

# Step 1: Push to ECR
 Store your Docker image in Amazon Elastic Container Registry (ECR).
 
 Create an ECR Repository: In the AWS Console, create a new private repository named my-crypto-app.
 
 Authenticate & Push: Select your new repository and click "View push commands". Follow the on-screen instructions to tag and push your local Docker image to ECR.

# Step 2: Deploy with ECS
Run and manage your container with Amazon Elastic Container Service (ECS).

 1. Create an ECS Cluster: A logical grouping for your services. A "Networking only" (Fargate) cluster is a great starting point.
 
 2. Create a Task Definition: This is the blueprint for your application.
 
 3. Select Fargate.
 
 4. Under "Container definitions", add a container named crypto-app-container and use your ECR image URI.
  
 5. Set Port mappings to expose container port 8000.
 
 6. Create an ECS Service: This will launch and maintain your tasks.
 
 7. Point the service to your new Task Definition.
 
 8. Set the desired number of tasks (e.g., 2 for high availability).
 
 9. Configure networking and security groups.
 
 Recommendation: Use an Application Load Balancer (ALB) to distribute traffic. Configure its target group to use the /health endpoint for health checks.

# ⚙️ Automated CI/CD Pipeline
 The buildspec.yml file enables automated deployments using AWS CodePipeline.
 
 1.) Source: Connect CodePipeline to your code repository (e.g., GitHub, AWS CodeCommit). When you connect to a source like GitHub, CodePipeline automatically creates a webhook in your repository. This webhook        is  what triggers the pipeline to run every time you git push new changes.
 
 1.) Build:
 
   Create a new AWS CodeBuild project and link it to your source.
 
   CodeBuild will automatically use the buildspec.yml file.
 
   Important: Grant the CodeBuild IAM role permissions to interact with ECR.
 
 2.) Deploy:
 
   Choose Amazon ECS as the deployment provider.

  Select your ECS cluster and service.

  The build stage will output an imagedefinitions.json file. Use this as the input for the deploy stage.

Now, every git push to your main branch will automatically build a new container image and deploy it to your ECS service.
