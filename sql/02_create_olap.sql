DROP TABLE IF EXISTS fact_benefit_payment CASCADE;
DROP TABLE IF EXISTS dim_date CASCADE;
DROP TABLE IF EXISTS dim_municipality CASCADE;
DROP TABLE IF EXISTS dim_benefit CASCADE;

-- Create Date Dimension (Dim_Aika)

CREATE TABLE dim_date
(
    date_id INT PRIMARY KEY,            -- e.g., 202601
    year_month VARCHAR(7) NOT NULL,     -- e.g., '2026-01'
    year INT NOT NULL,
    month_number INT NOT NULL
);

-- Create Municipality Dimension (Dim_Alue)

CREATE TABLE dim_municipality 
(
    municipality_code CHAR(3) PRIMARY KEY,
    municipality_name VARCHAR(100) NOT NULL
);

-- Create Benefit Dimension (Dim_Etuus)

CREATE TABLE dim_benefit 
(
    benefit_id INT PRIMARY KEY,
    benefit_name VARCHAR(100) NOT NULL,
    time_type VARCHAR(20) NOT NULL         -- e.g., 'Kuukausi'
);

-- Create Fact Table (Fakta_Etuusmaksut)

CREATE TABLE fact_benefit_payment
(
    date_id INT NOT NULL,
    municipality_code CHAR(3) NOT NULL,
    benefit_id INT NOT NULL,
    receiver_count INT NOT NULL,
    total_amount DECIMAL(15, 2) NOT NULL,

-- Composite Primary Key ensures uniqueness for each Month + Municipality + Benefit combination
CONSTRAINT pk_fact_benefit_payment PRIMARY KEY (date_id, municipality_code, benefit_id),

-- Foreign Keys linking facts to dimensions
CONSTRAINT fk_fact_date FOREIGN KEY (date_id) REFERENCES dim_date (date_id),
CONSTRAINT fk_fact_municipality FOREIGN KEY (municipality_code) REFERENCES dim_municipality (municipality_code),
CONSTRAINT fk_fact_benefit FOREIGN KEY (benefit_id) REFERENCES dim_benefit (benefit_id),

-- Data Quality Checks for aggregations
CONSTRAINT check_fact_receiver_count CHECK (receiver_count > 0),
CONSTRAINT check_fact_total_amount CHECK (total_amount >= 0)
);