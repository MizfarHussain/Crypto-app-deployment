# Use an official lightweight Python image as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir: Disables the cache to keep the image size smaller
# --trusted-host pypi.python.org: Sometimes needed in certain network environments
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY app.py .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches using gunicorn
# gunicorn is a production-ready WSGI server.
# --workers 3: Number of worker processes
# --bind 0.0.0.0:8000: Bind to all network interfaces on port 8000
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "app:app"]
