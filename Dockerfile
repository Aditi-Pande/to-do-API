FROM python:3.9

WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose Flask's port
EXPOSE 5000

# Set environment variables (optional)
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

# Default command
CMD ["python", "run.py"]
