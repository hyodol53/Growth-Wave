BEGIN TRANSACTION;

-- Add the 'category' column to the 'collaboration_interaction' table
ALTER TABLE collaboration_interaction
ADD COLUMN category VARCHAR NOT NULL DEFAULT 'SHARE';

COMMIT;
