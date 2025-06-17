FROM python:3.8
WORKDIR /app
# Optionally, install system dependencies
COPY . .
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev


RUN pip install --no-cache-dir -r requirements.txt
CMD ["Python3" , "main.py"]