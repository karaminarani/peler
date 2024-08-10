FROM python:3.9-alpine

# Set timezone
ENV TZ=Asia/Jakarta

# Install dependencies and clean up
RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
        gcc \
        musl-dev \
        libffi-dev \
        openssl-dev \
        python3-dev \
        build-base && \
    rm -rf /var/cache/apk/*

# Set the working directory
WORKDIR /app/

# Copy only requirements to leverage Docker cache for pip installs
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Command to run the application
CMD ["python", "main.py"]
