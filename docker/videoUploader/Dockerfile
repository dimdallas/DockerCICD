FROM python:3.8-slim

WORKDIR /app

COPY docker/videoUploader/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY docker/videoUploader/upload_service.py /app/
COPY docker/videoUploader/index.html docker/DAO/video_dao.py /app/
COPY docker/videoUploader/templates /app/templates

EXPOSE 5002

CMD ["python", "upload_service.py"]