CREATE OR REPLACE PROCEDURE update_prices_by_percent(
    percent_change NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Example: percent_change = 10 means +10%, -5 means -5%
    UPDATE supplied_by
    SET price = ROUND(price * (1 + percent_change / 100.0), 2);
END;
$$;
