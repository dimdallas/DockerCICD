FROM python:3.8-slim

WORKDIR /app

COPY docker/authenticator/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY docker/authenticator/auth_service.py docker/DAO/user_dao.py /app/

CMD ["python", "auth_service.py"]