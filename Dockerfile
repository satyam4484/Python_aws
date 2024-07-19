FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install  boto3

RUN ls /app

# Final command
CMD ["python", "./lambda_function.py"]