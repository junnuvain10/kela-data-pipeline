# Data Catalog: KELA Data Warehouse (Star Schema)

This document describes the structure of the OLAP data warehouse created by the ELT pipeline. The warehouse uses a Star Schema design optimized for querying aggregated benefit payment statistics while ensuring data anonymity.

## Fact Table

### `fact_benefit_payment`
Stores the aggregated, monthly statistics of benefit payments. This table contains only numerical facts and foreign keys to dimensions. All personally identifiable information (PII) has been stripped during the ETL process.

| Column Name | Data Type | Key Type | Description | Source / Derivation |
| :--- | :--- | :--- | :--- | :--- |
| `date_id` | INT | PK, FK | Unique identifier for the month | Derived from `OLTP.payment_transaction.payment_date` (format: YYYYMM) |
| `municipality_code` | CHAR(3) | PK, FK | Official municipality code | Sourced from `OLTP.customer.municipality_code` |
| `benefit_id` | INT | PK, FK | Unique identifier for the benefit | Sourced from `OLTP.payment_transaction.benefit_id` |
| `receiver_count` | INT | - | Count of unique individuals who received the benefit in the given month | Aggregated: `COUNT(DISTINCT OLTP.payment_transaction.customer_id)` |
| `total_amount` | DECIMAL(15,2) | - | Total amount of euros paid | Aggregated: `SUM(OLTP.payment_transaction.amount)` |

## Dimension Tables

### `dim_date`
Provides filtering and grouping capabilities based on time periods.

| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `date_id` | INT | PK | Unique identifier (e.g., 202601) |
| `year_month` | VARCHAR(7) | - | Human-readable year and month (e.g., '2026-01') |
| `year` | INT | - | The year of the transaction (e.g., 2026) |
| `month_number` | INT | - | The month of the transaction (1-12) |

### `dim_municipality`
Stores descriptive information about the geographical areas.

| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `municipality_code` | CHAR(3) | PK | Official municipality code (e.g., '109' for Hämeenlinna) |
| `municipality_name` | VARCHAR(100) | - | Full name of the municipality |

### `dim_benefit`
Stores descriptive information about the social benefits available.

| Column Name | Data Type | Key Type | Description |
| :--- | :--- | :--- | :--- |
| `benefit_id` | INT | PK | Unique identifier for the benefit |
| `benefit_name` | VARCHAR(100) | - | Name of the benefit (e.g., 'Lapsilisä', 'Opintotuki') |
| `time_type` | VARCHAR(20) | - | The cadence of the payment, defaults to 'Kuukausi' (Monthly) |