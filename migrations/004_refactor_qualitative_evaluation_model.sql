-- Refactor qualitative_evaluations table
-- Rename score to qualitative_score
ALTER TABLE qualitative_evaluations RENAME COLUMN score TO qualitative_score;

-- Add department_contribution_score
ALTER TABLE qualitative_evaluations ADD COLUMN department_contribution_score INTEGER NOT NULL DEFAULT 0;

-- Rename comment to feedback
ALTER TABLE qualitative_evaluations RENAME COLUMN comment TO feedback;
