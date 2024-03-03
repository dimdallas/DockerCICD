import mysql.connector
from mysql.connector import Error

class VideoDAO:
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


    def create_video(self, video_data):
        query = "INSERT INTO Videos (title, userId, url) VALUES (%s, %s, %s)"
        self.execute_query(query, (video_data['title'], video_data['userId'], video_data['url']))

    def get_videos_by_user_id(self, user_id):
        query = "SELECT * FROM Videos WHERE userId = %s"
        return self.fetch_all(query, (user_id,))
    
    def get_all_videos(self):
        query = "SELECT * FROM Videos"
        return self.fetch_all(query)
