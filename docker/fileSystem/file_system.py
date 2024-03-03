from flask import Flask, request, send_from_directory, jsonify, send_file, Response
import os
import uuid

VIDEOS_FOLDER = '/app/videos'
ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'mov', 'avi', 'flv'}

app = Flask(__name__)
app.config['VIDEOS_FOLDER'] = VIDEOS_FOLDER

def allowed_extension(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def generate_stream(filepath):
    with open(filepath, "rb") as video_file:
        while True:
            chunk = video_file.read(1024 * 1024) # Chunck of 1MB
            if not chunk:
                break
            yield chunk

@app.route('/', methods=['GET'])
def root():
    return "File System Service is running..."

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filename = str(uuid.uuid4())  # Generate a random unique string
    filepath = os.path.join(app.config['VIDEOS_FOLDER'], filename)
    
    # Check if the file is correctly saved
    if os.path.exists(filepath):
        return jsonify({'error': 'Failed to save the file on the filesystem, already exists'}), 500

    file.save(filepath)

    # Check if the file is correctly saved
    if not os.path.exists(filepath):
        return jsonify({'error': 'Failed to save the file on the filesystem'}), 500
    
    return jsonify({'url': filename}), 200

@app.route('/download', methods=['GET'])
def download():
    video_name = request.args.get('video')
    if not video_name:
        return jsonify({'error': 'Video identifier not provided'}), 400

    filepath = os.path.join(app.config['VIDEOS_FOLDER'], video_name)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    return send_from_directory(app.config['VIDEOS_FOLDER'], video_name, as_attachment=True)

@app.route('/stream', methods=['GET'])
def stream():
    video_name = request.args.get('video')
    if not video_name:
        return jsonify({'error': 'Video identifier not provided'}), 400

    filepath = os.path.join(app.config['VIDEOS_FOLDER'], video_name)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    return Response(generate_stream(filepath), content_type='video/mp4')

@app.route('/delete', methods=['DELETE'])
def delete():
    video_name = request.args.get('video')
    if not video_name:
        return jsonify({'error': 'Video identifier not provided'}), 400

    filepath = os.path.join(app.config['VIDEOS_FOLDER'], video_name)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    os.remove(filepath)
    return jsonify({'message': 'File deleted successfully'}), 200

if __name__ == '__main__':
    if not os.path.exists(VIDEOS_FOLDER):
        os.makedirs(VIDEOS_FOLDER)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
