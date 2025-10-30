-- Migration: Refactor 'projects' table
--
-- 1. Adds the 'evaluation_period_id' foreign key to associate projects with a specific evaluation period.
-- 2. Removes the unused 'description' column.
-- 3. Removes the UNIQUE constraint from the 'name' column.
--
-- NOTE: This migration is for SQLite and follows the recommended procedure for altering table constraints.
-- See: https://www.sqlite.org/lang_altertable.html
--
-- WARNING: Existing projects will be assigned a default 'evaluation_period_id' of 1.
-- Please verify this is appropriate for your data. If not, update the value manually after migration.

-- Disable foreign key checks to allow dropping the original 'projects' table
PRAGMA foreign_keys=OFF;

BEGIN TRANSACTION;

-- Step 1: Create a new table with the desired schema
CREATE TABLE projects_new (
    id INTEGER NOT NULL,
    name VARCHAR NOT NULL,
    start_date DATE,
    end_date DATE,
    pm_id INTEGER,
    evaluation_period_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(pm_id) REFERENCES users (id),
    FOREIGN KEY(evaluation_period_id) REFERENCES evaluation_periods (id)
);
CREATE INDEX ix_projects_new_name ON projects_new (name);

-- Step 2: Copy data from the old 'projects' table to the new one
-- A default evaluation_period_id of 1 is used for existing data.
INSERT INTO projects_new (id, name, start_date, end_date, pm_id, evaluation_period_id)
SELECT id, name, start_date, end_date, pm_id, 1
FROM projects;

-- Step 3: Drop the old table
DROP TABLE projects;

-- Step 4: Rename the new table to the original name
ALTER TABLE projects_new RENAME TO projects;

COMMIT;

-- Re-enable foreign key checks
PRAGMA foreign_keys=ON;
