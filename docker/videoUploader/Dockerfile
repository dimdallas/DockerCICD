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

COPY docker/videoUploader/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY docker/videoUploader/upload_service.py docker/DAO/video_dao.py /app/
COPY docker/videoUploader/templates /app/templates

EXPOSE 5002

CMD ["python", "upload_service.py"]