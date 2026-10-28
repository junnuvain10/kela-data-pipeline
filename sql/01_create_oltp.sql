DROP TABLE IF EXISTS payment_transaction CASCADE;
DROP TABLE IF EXISTS customer CASCADE;
DROP TABLE IF EXISTS benefit CASCADE;
DROP TABLE IF EXISTS municipality CASCADE;

-- Create municipality table (Kunta)

CREATE TABLE municipality 
(
    municipality_code CHAR(3) PRIMARY KEY,
    municipality_name VARCHAR(100) NOT NULL
);

-- Create benefit table (Etuus)

CREATE TABLE benefit 
(
    benefit_id SERIAL PRIMARY KEY,
    benefit_name VARCHAR(100) NOT NULL,
    time_type VARCHAR(20) DEFAULT 'Month'
);

-- Create customer table (Asiakas)

CREATE TABLE customer 
(
    customer_id SERIAL PRIMARY KEY,
    ssn VARCHAR(11) UNIQUE NOT NULL, -- Social Security Number (Hetu) must be unique
    full_name VARCHAR(255) NOT NULL,
    municipality_code CHAR(3) NOT NULL,
    
    CONSTRAINT fk_customer_municipality FOREIGN KEY (municipality_code) REFERENCES municipality (municipality_code),
    -- Basic sanity check for Finnish SSN length (either 10 or 11 chars depending on century char)
    CONSTRAINT check_customer_ssn_length CHECK (LENGTH(ssn) >= 10)
);

-- Create payment transaction table (Maksutapahtuma)

CREATE TABLE payment_transaction
(
    payment_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    benefit_id INT NOT NULL,
    payment_date DATE NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,

    CONSTRAINT fk_payment_customer FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
    CONSTRAINT fk_payment_benefit FOREIGN KEY (benefit_id) REFERENCES benefit (benefit_id),
    -- Data Quality: Amount must be greater than zero
    CONSTRAINT check_payment_amount CHECK (amount > 0)
);

-- Create performance indexes

CREATE INDEX idx_payment_date ON payment_transaction (payment_date);
CREATE INDEX idx_customer_municipality ON customer (municipality_code);