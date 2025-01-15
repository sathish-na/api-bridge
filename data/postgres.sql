-- PostgreSQL: Create Database and Tables with Dummy Data

-- Create Database
CREATE DATABASE SocialApp;
\c SocialApp;

-- Table: Users
CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Feeds
CREATE TABLE IF NOT EXISTS Feeds (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

-- Table: Likes
CREATE TABLE IF NOT EXISTS Likes (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    feed_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (feed_id) REFERENCES Feeds(id) ON DELETE CASCADE,
    UNIQUE (user_id, feed_id)
);

-- Table: Comments
CREATE TABLE IF NOT EXISTS Comments (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    feed_id INT NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (feed_id) REFERENCES Feeds(id) ON DELETE CASCADE
);

-- Insert Dummy Users
INSERT INTO Users (username, email, password) VALUES
('john_doe', 'john@example.com', 'password123'),
('jane_smith', 'jane@example.com', 'password123'),
('alice_jones', 'alice@example.com', 'password123');

-- Insert Dummy Feeds
INSERT INTO Feeds (user_id, content) VALUES
(1, 'Hello world! This is my first post.'),
(2, 'Loving the weather today!'),
(3, 'Can anyone recommend a good book to read?');

-- Insert Dummy Likes
INSERT INTO Likes (user_id, feed_id) VALUES
(1, 2),
(2, 3),
(3, 1);

-- Insert Dummy Comments
INSERT INTO Comments (user_id, feed_id, comment) VALUES
(1, 2, 'I love the weather too!'),
(2, 3, 'You should read "1984" by George Orwell.'),
(3, 1, 'Great to see your first post!');
