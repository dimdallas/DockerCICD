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

COPY docker/authenticator/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY docker/authenticator/auth_service.py docker/DAO/user_dao.py /app/

CMD ["python", "auth_service.py"]