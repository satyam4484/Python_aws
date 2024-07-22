# Use the official AWS Lambda Python 3.12 base image
FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.12


# Set the Lambda task root environment variable
ENV LAMBDA_TASK_ROOT=/var/task

# Copy the requirements.txt file to the Lambda task root
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Copy the lambda_function.py file to the Lambda task root
COPY main.py ${LAMBDA_TASK_ROOT}

# Copy the data_files directory to the Lambda task root
COPY data_files ${LAMBDA_TASK_ROOT}/data_files

# Debug step: List the contents of the Lambda task root to verify the files were copied correctly
RUN ls -al ${LAMBDA_TASK_ROOT}

# Install the required Python packages
RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt -t ${LAMBDA_TASK_ROOT}

# Debug step: List the contents of the Lambda task root after installing dependencies
RUN ls -al ${LAMBDA_TASK_ROOT}

# Create the required directories
RUN mkdir -p /tmp/data_files/output  /tmp/data_files/input

# Debug step: List the contents of the /tmp directory to verify the directories were created correctly
RUN ls -al /tmp/data_files

# Specify the Lambda function handler
CMD ["main.lambda_handler"]
