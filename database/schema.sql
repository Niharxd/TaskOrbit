-- TaskOrbit Database Schema
-- PostgreSQL
-- Run this file to manually recreate the database tables.
-- Note: Flask-SQLAlchemy creates these automatically on app startup.

-- Drop tables if they already exist (useful for a clean reset)
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS users;


-- Users table
CREATE TABLE users (
    id            SERIAL PRIMARY KEY,
    username      VARCHAR(80)  NOT NULL UNIQUE,
    email         VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    created_at    TIMESTAMP    NOT NULL DEFAULT NOW()
);


-- Tasks table
-- Each task belongs to a user via the user_id foreign key.
CREATE TABLE tasks (
    id           SERIAL PRIMARY KEY,
    user_id      INTEGER      NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title        VARCHAR(200) NOT NULL,
    description  TEXT,
    priority     VARCHAR(20)  NOT NULL DEFAULT 'Medium',  -- Low / Medium / High
    status       VARCHAR(20)  NOT NULL DEFAULT 'Pending', -- Pending / In Progress / Completed
    created_date TIMESTAMP    NOT NULL DEFAULT NOW()
);


-- Index on user_id for faster task lookups per user
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
