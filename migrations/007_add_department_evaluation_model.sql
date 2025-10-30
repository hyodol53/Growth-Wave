-- upgrade
ALTER TABLE organizations DROP COLUMN department_grade;

CREATE TABLE department_evaluations (
    id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    grade VARCHAR NOT NULL,
    evaluation_period_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(department_id) REFERENCES organizations (id),
    FOREIGN KEY(evaluation_period_id) REFERENCES evaluation_periods (id),
    UNIQUE (department_id, evaluation_period_id)
);

-- downgrade
ALTER TABLE organizations ADD COLUMN department_grade VARCHAR;

DROP TABLE department_evaluations;
