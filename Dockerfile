# Use a lightweight Python base image that is compatible with AMD64 architecture.
FROM python:3.10-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir numpy # Install numpy explicitly
RUN pip install --no-cache-dir -r requirements.txt

# Copy the trained model from your local 'models' directory
COPY models/heading_model.joblib /app/models/heading_model.joblib

# Copy the rest of the application code
COPY . .

# The command to run your solution for Round 1A. Using a JSON array format.
CMD ["python", "-m", "src.main", "--round", "1A", "/app/input", "/app/output"]