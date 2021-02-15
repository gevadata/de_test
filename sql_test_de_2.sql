SELECT
    site,
    (SUM(
    CASE
        WHEN promotion_code IS NOT NULL
        THEN number_of_visitors
        ELSE 0
    END)/SUM(number_of_visitors))*100 on_promotion_dates_percent
FROM
    site_visitors sv
LEFT JOIN
    promotion_dates pd
ON
    date >= start_date
AND date <= end_date
GROUP BY
    site

