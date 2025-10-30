-- Add reports_to column to users table for reporting structure
ALTER TABLE users ADD COLUMN reports_to INTEGER REFERENCES users(id);
