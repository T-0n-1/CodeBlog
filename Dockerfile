# Use official Python image
FROM python:3.12-slim

WORKDIR /app

# Copy requirements (Flask only)
COPY app.py init_db.py schema.sql ./
COPY templates/ ./templates/
COPY static/ ./static/

# Install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Initialize the database
RUN python init_db.py

# Expose port
EXPOSE 5000

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]
