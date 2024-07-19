FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir boto3

# Corrected MKDIR syntax
RUN mkdir -p /tmp/data_files/output

# Final command
CMD ["python", "./lambda_function.py"]