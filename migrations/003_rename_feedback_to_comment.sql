-- qualitative_evaluations 테이블의 feedback 컬럼을 comment로 변경합니다.
ALTER TABLE qualitative_evaluations RENAME COLUMN feedback TO comment;
