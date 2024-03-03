FROM python:3.8-slim

WORKDIR /app

COPY authenticator/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY authenticator/auth_service.py DAO/user_dao.py /app/

CMD ["python", "auth_service.py"]