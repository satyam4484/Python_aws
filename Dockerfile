FROM python:3.12-slim

WORKDIR /python_aws

COPY . /python_aws

RUN ls /python_aws

# Final command
CMD ["python", "./main.py"]