FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN ls /app

# Final command
CMD ["python", "./lambda_function.py"]