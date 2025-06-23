CREATE OR REPLACE FUNCTION check_price_limit()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.amount > 999.99 THEN
		RAISE EXCEPTION 'Amount %.2f is too high. Limit is 999.99.', NEW.amount;    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_check_price_limit ON ordered;

CREATE TRIGGER trg_check_price_limit
BEFORE INSERT OR UPDATE OF amount ON ordered
FOR EACH ROW
EXECUTE FUNCTION check_price_limit();
