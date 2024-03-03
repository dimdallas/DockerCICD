from flask import Flask, request, redirect, url_for, session, jsonify, render_template
import requests
import os
from video_dao import VideoDAO

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', b'_5#y2L"F4Q8z\n\xec]/')

authURL = "http://authenticator-container:5001/authenticate"
uploadURL = "http://file-system-container:5000/upload"

db_host = os.environ.get('MYSQL_HOST', "mysql-host")
db_user = os.environ.get('MYSQL_USER', "mysql-user")
db_password = os.environ.get('MYSQL_PASSWORD', "mysql-password")
db_database = os.environ.get('MYSQL_DATABASE', "mysql-database")

video_dao = VideoDAO(db_host, db_user, db_password, db_database)
video_dao.connect()

@app.route('/check', methods=['GET'])
def check():
    return "Video Uploading Service is running..."

@app.route('/')
def index():
    if 'username' in session and 'session_token' in session:
        # If user is already authenticated, redirect to main page
        return redirect(url_for('upload_video'))

    return render_template('credential_input.html')

@app.route('/logout', methods=['POST'])
def logout():
    # Clear the user's session
    session.clear()

    return redirect(url_for('index'))

@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.form
    username = data.get('username')
    password = data.get('password')

    # Authenticate user by posting credentials to the authentication service
    response = requests.post(authURL, json={'username': username, 'password': password})

    if response.status_code == 200:
        user_info = response.json()
        session['userId'] = user_info['userId']
        session['username'] = user_info['username']
        session['session_token'] = user_info['session_token']

        # Redirect to main page
        return redirect(url_for('upload_video'))
    else:
        # Authentication failed, redirect back to the credential input form
        return redirect(url_for('index'))
    
@app.route('/upload-video')
def upload_video():
    if 'username' not in session or 'session_token' not in session:
        # If user is not authenticated, redirect to the credential input form
        return redirect(url_for('index'))

    return render_template('upload_video.html', username=session['username'])

@app.route('/handle-upload', methods=['POST'])
def handle_upload():
    if 'username' not in session or 'session_token' not in session:
        # If user is not authenticated, redirect to the credential input form
        return redirect(url_for('index'))

    # Get user information from session
    userId = session['userId']

    title = request.form.get('title')
    video_file = request.files.get('video')

    if not title or not video_file:
        return jsonify({'error': 'Title and video file are required'}), 400

    try:
        # Post the video file to the file system service
        response = requests.post(uploadURL, files={'file': (video_file.filename, video_file.read())})

        if response.status_code == 200:
            # Video file uploaded successfully
            video_url = response.json()['url']

            # Insert the video entry to the database using DAO
            video_data = {'title': title, 'userId': userId, 'url': video_url}
            video_dao.create_video(video_data)

            return jsonify({'message': 'Video uploaded successfully'}), 200
        else:
            return jsonify({'error': 'Failed to upload video file'}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
