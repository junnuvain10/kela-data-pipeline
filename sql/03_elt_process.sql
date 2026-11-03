-- ==============================================================================
-- Kela Data Pipeline: ELT Process
-- Transfers and aggregates data from the OLTP schema to the OLAP schema (Star Schema)
-- ==============================================================================

-- 1. Truncate analytical tables (Fact table first for referential integrity)
TRUNCATE TABLE fact_benefit_payment CASCADE;
TRUNCATE TABLE dim_date CASCADE;
TRUNCATE TABLE dim_municipality CASCADE;
TRUNCATE TABLE dim_benefit CASCADE;

-- 2. Load static dimensions directly from OLTP reference data
INSERT INTO dim_municipality (municipality_code, municipality_name)
SELECT 
    municipality_code, 
    municipality_name 
FROM municipality;

INSERT INTO dim_benefit (benefit_id, benefit_name, time_type)
SELECT 
    benefit_id, 
    benefit_name, 
    time_type 
FROM benefit;

-- 3. Generate date dimension dynamically based on payment transactions
INSERT INTO dim_date (date_id, year_month, year, month_number)
SELECT DISTINCT 
    CAST(TO_CHAR(payment_date, 'YYYYMM') AS INT) AS date_id,
    TO_CHAR(payment_date, 'YYYY-MM') AS year_month,
    CAST(EXTRACT(YEAR FROM payment_date) AS INT) AS year,
    CAST(EXTRACT(MONTH FROM payment_date) AS INT) AS month_number
FROM payment_transaction;

-- 4. Core ELT process: Aggregate data into the fact table
INSERT INTO fact_benefit_payment (date_id, municipality_code, benefit_id, receiver_count, total_amount)
SELECT 
    CAST(TO_CHAR(pt.payment_date, 'YYYYMM') AS INT) AS date_id,
    c.municipality_code,
    pt.benefit_id,
    COUNT(DISTINCT pt.customer_id) AS receiver_count,
    SUM(pt.amount) AS total_amount
FROM payment_transaction pt
JOIN customer c ON pt.customer_id = c.customer_id
GROUP BY 
    CAST(TO_CHAR(pt.payment_date, 'YYYYMM') AS INT),
    c.municipality_code,
    pt.benefit_id;