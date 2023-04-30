FROM python:3.10

# Copy project files
WORKDIR /noted
COPY . .

# Set python env
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Change project scripts permissions
RUN chmod 700 /noted/logs/logs_report.sh

# Install requirements and clean all cache
RUN pip install -r requirements/production.txt \
    && apt-get update \
    && apt-get -y install wkhtmltopdf \
    && apt-get -y autoclean
    
