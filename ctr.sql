-- Click-Through Rate (CTR) per app for the year 2022
--
-- Schema:
--   events (app_id INTEGER, event_type VARCHAR, timestamp DATETIME)
--
-- CTR = (clicks / impressions) * 100

SELECT
    app_id,
    ROUND(
        100.0
        * SUM(CASE WHEN event_type = 'click'      THEN 1 ELSE 0 END)
        / SUM(CASE WHEN event_type = 'impression' THEN 1 ELSE 0 END),
        2
    ) AS ctr
FROM events
WHERE strftime('%Y', timestamp) = '2022'
GROUP BY app_id;
