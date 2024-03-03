FROM python:3.8-slim

WORKDIR /app

COPY videoUploader/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# COPY videoUploader/upload_service.py /app/
COPY videoUploader/index.html DAO/video_dao.py /app/
COPY videoUploader/templates /app/templates

EXPOSE 5002

CMD ["python", "upload_service.py"]