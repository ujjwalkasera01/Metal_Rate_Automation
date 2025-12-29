# Use Python 3.10 for telegram bot compatibility
FROM python:3.10-slim

# Create working directory
WORKDIR /app

# Install dependencies first (better build cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose Render's required port
ENV PORT=10000

# Command to start app
CMD ["uvicorn", "api.app:app", "--host=0.0.0.0", "--port=10000"]
