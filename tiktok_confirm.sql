-- Find users who confirmed their sign-up on the second day (not the first day).
--
-- Schema:
--   emails (email_id INTEGER, user_id INTEGER, signup_date DATETIME)
--   texts  (text_id INTEGER, email_id INTEGER, signup_action VARCHAR, action_date DATETIME)
--
-- signup_action values: 'Confirmed', 'Not Confirmed'

SELECT
    e.user_id
FROM emails e
JOIN texts t
    ON e.email_id = t.email_id
WHERE t.signup_action = 'Confirmed'
    AND t.action_date = e.signup_date + INTERVAL '1 day';
