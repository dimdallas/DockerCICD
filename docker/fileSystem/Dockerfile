FROM python:3.8-slim

WORKDIR /app

COPY fileSystem/requirements.txt /app
# RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# COPY fileSystem/file_system.py /app/

EXPOSE 5000

CMD ["python", "file_system.py"]