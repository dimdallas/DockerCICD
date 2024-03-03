import os
import uuid
from flask import Flask, request, jsonify, session
from user_dao import UserDAO

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', b'_5#y2L"F4Q8z\n\xec]/')

# Use environment variables for database credentials
db_host = os.environ.get('MYSQL_HOST', "mysql-host")
db_user = os.environ.get('MYSQL_USER', "mysql-user")
db_password = os.environ.get('MYSQL_PASSWORD', "mysql-password")
db_database = os.environ.get('MYSQL_DATABASE', "mysql-database")

user_dao = UserDAO(db_host, db_user, db_password, db_database)
user_dao.connect()

@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    print(username + " " + password)

    # Authenticate user using the DAO
    user = user_dao.authenticate_user(username, password)
    print(user)

    if user:
        # Create a session token and store user information
        session['userId'] = user['userId']
        session['username'] = user['username']
        # Generate a unique session ID using uuid
        session['sid'] = str(uuid.uuid4())

        response_data = {
            'message': 'Authentication successful',
            'session_token': session['sid'],
            'userId' : session['userId'],
            'username' : session['username']
        }
        return jsonify(response_data), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/authorized', methods=['GET'])
def protected_endpoint():
    if 'user_id' in session:
        return jsonify({'message': 'Protected endpoint accessed by user with ID: {}'.format(session['user_id'])}), 200
    else:
        return jsonify({'error': 'Unauthorized'}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
