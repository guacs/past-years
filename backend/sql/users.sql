CREATE TABLE users(
    user_id VARCHAR(32) PRIMARY KEY,
    display_name TINYTEXT NOT NULL,
    email VARCHAR(255) UNIQUE,
    hashed_pwd BINARY(64) NOT NULL,
    salt BINARY(16) NOT NULL
)