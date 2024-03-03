FROM python:3.8-slim

WORKDIR /app

COPY docker/videoStreamer/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY docker/videoStreamer/video_streamer.py /app/
COPY docker/videoStreamer/index.html docker/DAO/* /app/
COPY docker/videoStreamer/templates /app/templates

EXPOSE 5003

CMD ["python", "video_streamer.py"]