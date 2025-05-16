# Start from the AWS Lambda Python 3.10 base image
FROM public.ecr.aws/lambda/python:3.10


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Install only required dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model, scaler, and app code
COPY rf_model.pkl .
COPY scaler.pkl .
COPY app.py .

# Command to run Lambda
CMD ["app.handler"]
