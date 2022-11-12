FROM python:3.8.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

WORKDIR /noted 

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt  


 

