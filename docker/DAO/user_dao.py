import mysql.connector
from mysql.connector import Error

class UserDAO:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")

    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Disconnected from MySQL database")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            self.connection.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def fetch_one(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        result = None
        try:
            cursor.execute(query, params)
            result = cursor.fetchone()
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
        return result
    
    def fetch_all(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)
        result = None
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
        return result

    def create_user(self, user_data):
        query = "INSERT INTO Users (name, username, password) VALUES (%s, %s, %s)"
        self.execute_query(query, (user_data['name'], user_data['username'], user_data['password']))

    def get_user_by_username(self, username):
        query = "SELECT * FROM Users WHERE username = %s"
        return self.fetch_one(query, (username,))

    def authenticate_user(self, username, password):
        query = "SELECT * FROM Users WHERE username = %s AND password = %s"
        return self.fetch_one(query, (username, password))
    
    def get_all_users(self):
        query = "SELECT userId, username FROM Users"
        return self.fetch_all(query)