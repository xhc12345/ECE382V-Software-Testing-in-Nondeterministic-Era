# Use an official Python 3.11 runtime as a base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /src

# Copy the requirements file and install dependencies
COPY src/requirements.txt /src/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ /src/

# Run the application
CMD ["python", "main.py"]
