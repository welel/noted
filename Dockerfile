FROM python:3.10

# Copy project files
WORKDIR /noted
COPY . .

# Set python env
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Set timezone
RUN set -eux; \
        rm /etc/localtime; \
        ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime; \
        date

# Change project scripts permissions
RUN chmod 700 /noted/logs/logs_report.sh

# Install requirements and clean all cache
RUN pip install -r /noted/requirements/production.txt \
    && rm -rf /noted/requirements \
    && apt-get update \
    && apt-get -y install wkhtmltopdf \
    && apt-get -y install ncat \
    && apt-get -y autoclean
