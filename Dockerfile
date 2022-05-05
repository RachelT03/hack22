FROM python:3.7

RUN mkdir usr/app
WORKDIR usr/app

COPY . .app

RUN pip install -r requirements.txt

CMD python app.py