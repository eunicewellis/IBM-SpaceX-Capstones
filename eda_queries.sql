-- SpaceX Falcon 9 course dataset: SQL EDA examples
-- Load the course CSV into a SQLite table named SPACEXTABLE before running these queries.
-- Inspect schema first: PRAGMA table_info(SPACEXTABLE);

-- 1. First five records
SELECT * FROM SPACEXTABLE LIMIT 5;

-- 2. Number of records
SELECT COUNT(*) AS total_launches FROM SPACEXTABLE;

-- 3. Unique launch sites
SELECT DISTINCT Launch_Site FROM SPACEXTABLE;

-- 4. Launch counts by site
SELECT Launch_Site, COUNT(*) AS launches
FROM SPACEXTABLE
GROUP BY Launch_Site
ORDER BY launches DESC;

-- 5. Payloads greater than 10,000 kg
SELECT * FROM SPACEXTABLE
WHERE PAYLOAD_MASS__KG_ > 10000
LIMIT 5;

-- 6. Average payload mass by booster version
SELECT Booster_Version, AVG(PAYLOAD_MASS__KG_) AS avg_payload_kg
FROM SPACEXTABLE
GROUP BY Booster_Version
ORDER BY avg_payload_kg DESC;

-- 7. Landing outcomes for successful course labels
SELECT Landing_Outcome, COUNT(*) AS successful_records
FROM SPACEXTABLE
WHERE Class = 1
GROUP BY Landing_Outcome
ORDER BY successful_records DESC;

-- 8. Launches and landing success rate by site
SELECT Launch_Site, COUNT(*) AS total_launches, SUM(Class) AS successful_landings,
       ROUND(AVG(Class) * 100, 2) AS success_rate_pct
FROM SPACEXTABLE
GROUP BY Launch_Site
ORDER BY success_rate_pct DESC;

-- 9. Successful records for booster versions containing Block 5
SELECT Booster_Version, COUNT(*) AS successful_landings
FROM SPACEXTABLE
WHERE Class = 1 AND Booster_Version LIKE '%Block 5%'
GROUP BY Booster_Version;

-- 10. Payload statistics among successful records
SELECT MIN(PAYLOAD_MASS__KG_) AS min_payload_kg,
       AVG(PAYLOAD_MASS__KG_) AS avg_payload_kg,
       MAX(PAYLOAD_MASS__KG_) AS max_payload_kg
FROM SPACEXTABLE
WHERE Class = 1;
