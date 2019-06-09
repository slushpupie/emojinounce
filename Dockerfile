FROM python:3

ENV SLACK_EVENTS_ENDPOINT /slack_events
#ENV SLACK_ANNOUNCE_CHANNEL_ID
#ENV SLACK_SIGNING_SECRET
#ENV SLACK_BOT_TOKEN

RUN pip3 install gunicorn
COPY requirements.txt setup.py /app/
WORKDIR /app
RUN pip3 install -r requirements.txt

COPY app.py /app/
COPY emojinounce /app/emojinounce
RUN pip3 install .

ADD start.sh /app/main

ENTRYPOINT /app/main
