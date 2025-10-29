-- Migration to add comment fields to evaluation tables and rename feedback column.
-- This script is for SQLite.

-- Begin a transaction to ensure all changes are applied atomically.
BEGIN TRANSACTION;

-- Step 1: Rename 'feedback' column to 'comment' in the 'peer_evaluations' table.
-- SQLite does not support renaming columns directly, so the table must be rebuilt.

-- 1.1. Create a new table with the desired schema.
CREATE TABLE peer_evaluations_new (
    id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    evaluator_id INTEGER NOT NULL,
    evaluatee_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    evaluation_period VARCHAR NOT NULL,
    comment VARCHAR,
    PRIMARY KEY (id),
    FOREIGN KEY(project_id) REFERENCES projects (id),
    FOREIGN KEY(evaluator_id) REFERENCES users (id),
    FOREIGN KEY(evaluatee_id) REFERENCES users (id)
);

-- 1.2. Copy the data from the old table to the new table, mapping 'feedback' to 'comment'.
INSERT INTO peer_evaluations_new (id, project_id, evaluator_id, evaluatee_id, score, evaluation_period, comment)
SELECT id, project_id, evaluator_id, evaluatee_id, score, evaluation_period, feedback
FROM peer_evaluations;

-- 1.3. Drop the old table.
DROP TABLE peer_evaluations;

-- 1.4. Rename the new table to the original name.
ALTER TABLE peer_evaluations_new RENAME TO peer_evaluations;


-- Step 2: Add the 'comment' column to the 'pm_evaluations' table.
ALTER TABLE pm_evaluations ADD COLUMN comment VARCHAR;


-- Commit the transaction to finalize the changes.
COMMIT;
