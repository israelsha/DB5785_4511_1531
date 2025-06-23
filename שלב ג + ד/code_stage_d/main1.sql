DO $$
DECLARE
    r RECORD;
BEGIN
    -- Call to a procedure that tries to add an order (if there is stock)
    CALL add_order_if_in_stock(240, 2, 235, 2, 101);

   -- Call to a function that returns an employee's work hours report
    FOR r IN SELECT * FROM get_employee_monthly_report(3, 4, 2024)
    LOOP
        RAISE NOTICE 'Employee % worked % days, total %, average % per day',
            r.employee_id, r.working_days, r.total_worked, r.average_per_day;
    END LOOP;
END;
$$;
