FROM python:3.12-slim
LABEL maintainer="Imran"

# Set working directory
WORKDIR /usr/src/app/

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libffi-dev \
    git \
    nginx \
    libpango1.0-dev \
    libopenjp2-7-dev \
    fontconfig \
    zlib1g-dev \
    libjpeg-dev \
    netcat-openbsd \ 
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Ensure the entrypoint script is executable
RUN chmod +x scripts/entrypoint.sh

# Expose port
EXPOSE 80

ENTRYPOINT ["./scripts/entrypoint.sh"]
