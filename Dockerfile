# Use the base image
FROM nvcr.io/nvidia/l4t-tensorflow:r35.3.1-tf2.11-py3

# Install additional dependencies
RUN apt-get update && apt-get install -y \
    git \
    python3.8 \
    python3.8-venv \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment and work in it
RUN python3.8 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Clone TensorFlow models repository
RUN git clone https://github.com/tensorflow/models.git /tensorflow/models

# Change directory to models/research
WORKDIR /tensorflow/models/research

# Install protobuf compiler and compile proto files
RUN apt-get update && apt-get install -y \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

RUN protoc object_detection/protos/*.proto --python_out=.

# Copy setup.py file
RUN cp object_detection/packages/tf2/setup.py .

# Install TensorFlow Object Detection API
RUN python -m pip install .

# Set the working directory to /tensorflow/models
WORKDIR /tensorflow/models
