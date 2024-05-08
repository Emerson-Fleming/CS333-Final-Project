# Base image for the application
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements.txt (if you use it) or directly copy your application code
COPY requirements.txt .
RUN pip install --upgrade pip -r requirements.txt

# OR (if you don't use requirements.txt)
# Copy your application code
COPY . .

# Install additional tools (if needed)
RUN python3 -m pip install --upgrade pip flake8 pytest pyshark matplotlib pandas coverage

# Set the command to run your application (optional)
CMD [ "python", "test_unit_integration.py" ]  # Replace with your application entry point
