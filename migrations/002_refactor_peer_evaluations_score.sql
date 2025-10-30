-- Migration to refactor the peer_evaluations table for multi-item scoring.
-- This script is for SQLite and is designed to be transactional and preserve data.

BEGIN TRANSACTION;

-- Step 1: Create the new table with the updated schema
CREATE TABLE peer_evaluations_new (
    id INTEGER NOT NULL, 
    project_id INTEGER NOT NULL, 
    evaluator_id INTEGER NOT NULL, 
    evaluatee_id INTEGER NOT NULL, 
    score_1 INTEGER NOT NULL, 
    score_2 INTEGER NOT NULL, 
    score_3 INTEGER NOT NULL, 
    score_4 INTEGER NOT NULL, 
    score_5 INTEGER NOT NULL, 
    score_6 INTEGER NOT NULL, 
    score_7 INTEGER NOT NULL, 
    evaluation_period VARCHAR NOT NULL, 
    comment VARCHAR, 
    PRIMARY KEY (id), 
    FOREIGN KEY(project_id) REFERENCES projects (id), 
    FOREIGN KEY(evaluator_id) REFERENCES users (id), 
    FOREIGN KEY(evaluatee_id) REFERENCES users (id)
);

-- Step 2: Copy data from the old table to the new table.
-- The value from the old 'score' column is moved to 'score_1', and other scores are set to 0.
INSERT INTO peer_evaluations_new (id, project_id, evaluator_id, evaluatee_id, score_1, score_2, score_3, score_4, score_5, score_6, score_7, evaluation_period, comment)
SELECT id, project_id, evaluator_id, evaluatee_id, score, 0, 0, 0, 0, 0, 0, evaluation_period, comment FROM peer_evaluations;

-- Step 3: Drop the old table
DROP TABLE peer_evaluations;

-- Step 4: Rename the new table to the original name
ALTER TABLE peer_evaluations_new RENAME TO peer_evaluations;

COMMIT;
