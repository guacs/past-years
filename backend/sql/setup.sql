-- Holds the various SQL queries to run to set up the initial database.

CREATE DATABASE IF NOT EXISTS past_years;

CREATE TABLE IF NOT EXISTS users(
    user_id VARCHAR(32) PRIMARY KEY,
    display_name TINYTEXT NOT NULL,
    email VARCHAR(255) UNIQUE,
    hashed_pwd BINARY(64) NOT NULL,
    salt BINARY(16) NOT NULL
);

CREATE TABLE IF NOT EXISTS tokens(
    user_id VARCHAR(32) PRIMARY KEY,
    refresh_token VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
