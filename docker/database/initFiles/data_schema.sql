-- Create Users table
CREATE TABLE Users (
    userId INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create Videos table
CREATE TABLE Videos (
    videoId INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    userId INT NOT NULL,
    url VARCHAR(255) NOT NULL,
    FOREIGN KEY (userId) REFERENCES Users(userId)
);
