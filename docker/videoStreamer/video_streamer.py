from flask import Flask, send_file, request, redirect, url_for, session, jsonify, render_template
import requests
import os
from video_dao import VideoDAO
from user_dao import UserDAO

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', b'_5#y2L"F4Q8z\n\xec]/')

authURL = "http://authenticator-container:5001/authenticate"
streamURL = "http://file-system-container:5000/stream"

db_host = os.environ.get('MYSQL_HOST', "mysql-host")
db_user = os.environ.get('MYSQL_USER', "mysql-user")
db_password = os.environ.get('MYSQL_PASSWORD', "mysql-password")
db_database = os.environ.get('MYSQL_DATABASE', "mysql-database")

video_dao = VideoDAO(db_host, db_user, db_password, db_database)
video_dao.connect()

user_dao = UserDAO(db_host, db_user, db_password, db_database)
user_dao.connect()

@app.route('/check', methods=['GET'])
def check():
    return "Video Streaming Service is running..."

@app.route('/')
def index():
    if 'username' in session and 'session_token' in session:
        # If user is already authenticated, redirect to main page
        return redirect(url_for('stream_video'))

    return render_template('credential_input.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    # Authenticate user by posting credentials to the authentication service
    response = requests.post(authURL, json={'username': username, 'password': password})

    if response.status_code == 200:
        # User authenticated successfully
        user_info = response.json()
        session['user_id'] = user_info['user_id']
        session['username'] = user_info['username']
        session['session_token'] = user_info['session_token']

        # Redirect to main page
        return redirect(url_for('upload_video'))
    else:
        # Authentication failed, redirect back to the credential input form
        return redirect(url_for('index'))
    
@app.route('/stream-video')
def stream_video():
    if 'username' not in session or 'session_token' not in session:
        # If user is not authenticated, redirect to the credential input form
        return redirect(url_for('index'))

    # Serve the main page passing username
    return render_template('stream_video.html', username=session['username'])

@app.route('/get-users', methods=['GET'])
def get_users():
    if 'username' not in session or 'session_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    # Get all users from the database using DAO
    users = user_dao.get_all_users()

    return jsonify(users), 200

@app.route('/get-videos', methods=['GET'])
def get_videos():
    if 'username' not in session or 'session_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = request.args.get('user')

    if user_id:
        # Get videos by userId from database
        videos = video_dao.get_videos_by_user_id(user_id)
    else:
        # Get all videos from database
        videos = video_dao.get_all_videos()

    return jsonify(videos), 200

@app.route('/handle-stream', methods=['GET'])
def handle_stream():
    if 'username' not in session or 'session_token' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    video_url = request.args.get('video')

    if not video_url:
        return jsonify({'error': 'Video URL is required'}), 400

    # Request video stream from file system container
    response = requests.get(f"{streamURL}?video={video_url}", stream=True)

    if response.status_code == 200:
        # Stream the video
        return send_file(response.raw, mimetype="video/mp4")
        # return response.content, response.status_code, {'Content-Type': 'video/mp4'}
    else:
        return jsonify({'error': 'Failed to retrieve video stream'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
