FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY bot.py .
COPY training.py .
COPY config.yaml .

# Create directory for training data
RUN mkdir -p training_data

# Run the bot
CMD ["python", "bot.py"]
