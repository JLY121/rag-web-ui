FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
  build-essential \
  default-libmysqlclient-dev \ 
  pkg-config \
  netcat-traditional \
  curl \
  && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script first
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Copy application files
# 将当前目录下（backend）的所有文件复制到工作目录下（/app）
COPY . .  

# Create uploads directory
RUN mkdir -p uploads

# Set Python path and environment
ENV PYTHONPATH=/app
ENV ENVIRONMENT=production

# Run the application
# 调用main启动函数的位置，用uvicorn启动fastapi应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
