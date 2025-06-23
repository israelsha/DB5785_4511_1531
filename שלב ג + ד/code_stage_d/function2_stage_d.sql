CREATE OR REPLACE FUNCTION report_price_gap_between_suppliers(item_limit INT)
RETURNS TABLE (
    item_id INT,
    min_price NUMERIC(10,2),
    max_price NUMERIC(10,2),
    gap_percent NUMERIC(10,2)
) AS $$
BEGIN
    -- Return a result set (table) with item_id, min and max prices, and the price gap percentage
    RETURN QUERY
    SELECT
        sb.item_id,                                     -- ID of the item
        MIN(sb.price) AS min_price,                     -- Lowest price among all suppliers for the item
        MAX(sb.price) AS max_price,                     -- Highest price among all suppliers for the item
        ROUND(((MAX(sb.price) - MIN(sb.price)) / MIN(sb.price)) * 100, 2) AS gap_percent
                                                        -- Percentage difference between max and min price
    FROM supplied_by sb
    GROUP BY sb.item_id                                 -- Group by item to calculate min/max per item
    HAVING COUNT(*) > 1                                 -- Only include items that are supplied by more than one supplier
    ORDER BY gap_percent DESC                           -- Sort the results by price gap descending
    LIMIT item_limit;                                   -- Limit the number of returned rows to the given argument
END;
$$ LANGUAGE plpgsql;
