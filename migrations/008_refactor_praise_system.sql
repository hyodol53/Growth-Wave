BEGIN TRANSACTION;

-- Step 1: Drop foreign key constraints pointing to old tables
-- Note: SQLite does not robustly support dropping foreign key constraints.
-- The typical way is to rebuild the tables, but that's complex.
-- For this migration, we assume we can drop the tables directly,
-- which works if the database is not enforcing foreign keys during this transaction,
-- or if we drop the dependent tables first.
-- Let's start by dropping the User table relationships to PraiseLimiter.
-- As we are rebuilding the app, we will drop the tables.

-- Step 2: Drop old tables that are no longer needed
DROP TABLE IF EXISTS praise_strength_association;
DROP TABLE IF EXISTS praise_limiter;
DROP TABLE IF EXISTS praise;
DROP TABLE IF EXISTS strength;

-- Step 3: Create the new 'praise' table according to the new model
CREATE TABLE praise (
    id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,
    evaluation_period_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    hashtag VARCHAR NOT NULL,
    created_at DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY(sender_id) REFERENCES users (id),
    FOREIGN KEY(recipient_id) REFERENCES users (id),
    FOREIGN KEY(evaluation_period_id) REFERENCES evaluation_periods (id)
);
CREATE INDEX ix_praise_id ON praise (id);
CREATE INDEX ix_praise_recipient_id ON praise (recipient_id);
CREATE INDEX ix_praise_evaluation_period_id ON praise (evaluation_period_id);


-- Step 4: Create the new 'strength_profile' table for aggregation
CREATE TABLE strength_profile (
    user_id INTEGER NOT NULL,
    hashtag VARCHAR NOT NULL,
    evaluation_period_id INTEGER NOT NULL,
    count INTEGER NOT NULL,
    PRIMARY KEY (user_id, hashtag, evaluation_period_id),
    FOREIGN KEY(user_id) REFERENCES users (id),
    FOREIGN KEY(evaluation_period_id) REFERENCES evaluation_periods (id)
);

COMMIT;
