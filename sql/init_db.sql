CREATE DATABASE IF NOT EXISTS ready_for_sky;
USE ready_for_sky;

CREATE TABLE IF NOT EXISTS open_rsa_keys
(
    user_name    VARCHAR(100),
    open_rsa_key TEXT
);
CREATE UNIQUE INDEX user_name__idx ON open_rsa_keys (user_name);
