-- Insert sample user data
INSERT INTO Users (name, username, password) VALUES
    ('User1', 'user1', 'password1'),
    ('User2', 'user2', 'password2');

-- Insert sample video data
-- INSERT INTO Videos (title, userId, url) VALUES
--     ('Video 1', (SELECT userId FROM Users WHERE username = 'user1'), '/video1'),
--     ('Video 2', (SELECT userId FROM Users WHERE username = 'user2'), '/video2');