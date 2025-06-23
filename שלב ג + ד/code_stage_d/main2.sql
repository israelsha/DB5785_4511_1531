DO $$
DECLARE
    r RECORD;
BEGIN
    -- Call to a procedure that updates prices by a certain percentage
    CALL update_prices_by_percent(5); -- Price increase by 5%

    -- Calling a function that returns a table of price differences between suppliers
    FOR r IN SELECT * FROM report_price_gap_between_suppliers(5)
    LOOP
        RAISE NOTICE 'Item %: min=%, max=%, gap=%%%',
            r.item_id, r.min_price, r.max_price, r.gap_percent;
    END LOOP;
END;
$$;
