FROM python:3.8.10

WORKDIR /noted
COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
ENV VIRTUAL_ENV "/noted/env"

RUN python -m venv $VIRTUAL_ENV

ENV PATH "VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

 

