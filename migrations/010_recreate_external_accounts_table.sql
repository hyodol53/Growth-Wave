BEGIN TRANSACTION;

-- Drop the existing external_accounts table if it exists
DROP TABLE IF EXISTS external_accounts;

-- Create the new external_accounts table with the updated schema
CREATE TABLE external_accounts (
    id INTEGER NOT NULL,
    provider VARCHAR(255) NOT NULL,
    account_id VARCHAR NOT NULL,
    encrypted_credentials VARCHAR NOT NULL,
    owner_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(owner_id) REFERENCES users (id)
);

CREATE INDEX ix_external_accounts_id ON external_accounts (id);

COMMIT;
