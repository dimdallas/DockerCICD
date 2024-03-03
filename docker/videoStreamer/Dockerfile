FROM python:3.8-slim

ARG DB_DATABASE
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST

ENV MYSQL_DATABASE=${DB_DATABASE} \
    MYSQL_USER=${DB_USER} \
    MYSQL_PASSWORD=${DB_PASSWORD} \
    MYSQL_HOST=${DB_HOST}

WORKDIR /app

COPY docker/videoStreamer/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY docker/videoStreamer/video_streamer.py docker/DAO/* /app/
COPY docker/videoStreamer/templates /app/templates

EXPOSE 5003

CMD ["python", "video_streamer.py"]