CREATE TABLE IF NOT EXISTS data (
            user_ip VARCHAR(255) PRIMARY KEY,
            country_code VARCHAR(3) NOT NULL,
            country_name VARCHAR(255) NOT NULL,
            distance FLOAT NOT NULL,
            calls_counter INTEGER NOT NULL

        );

CREATE TABLE IF NOT EXISTS logs (
            log_id SERIAL PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            date_time VARCHAR(255) NOT NULL
        );