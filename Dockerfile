FROM python:3.8.10

WORKDIR /noted
COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

RUN pip install -r requirements.txt \
    && apt-get install wkhtmltopdf -y \
    && apt-get autoclean -y
