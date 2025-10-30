BEGIN TRANSACTION;

CREATE TABLE retrospectives (
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    evaluation_period_id INTEGER,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_at DATETIME,
    updated_at DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users (id),
    FOREIGN KEY(evaluation_period_id) REFERENCES evaluation_periods (id)
);

CREATE INDEX ix_retrospectives_id ON retrospectives (id);
CREATE INDEX ix_retrospectives_user_id ON retrospectives (user_id);

COMMIT;
