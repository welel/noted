FROM python:3.10

# Copy project files to container
WORKDIR /noted
COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Install requirements and clean cache
RUN pip install -r requirements/production.txt \
    && apt-get update \
    && apt-get -y install wkhtmltopdf \
    && apt-get -y autoclean

# Cron settings
RUN chmod 700 /noted/logs/logs_report.sh \
    && echo "0 * * * * root /noted/logs/logs_report.sh" >> /etc/cron.d/e2scrub_all
