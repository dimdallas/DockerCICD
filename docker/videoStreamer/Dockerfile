FROM python:3.8-slim

WORKDIR /app

COPY videoStreamer/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# COPY videoStreamer/video_streamer.py /app/
COPY videoStreamer/index.html DAO/* /app/
COPY videoStreamer/templates /app/templates

EXPOSE 5003

CMD ["python", "video_streamer.py"]