CREATE OR REPLACE FUNCTION get_employee_monthly_report(
    emp_id INT,
    month_input INT,
    year_input INT
)
RETURNS TABLE (
    employee_id INT,
    working_days INT,
    total_worked INTERVAL,
    average_per_day INTERVAL
) AS $$
DECLARE
    rec RECORD;
    total_hours INTERVAL := '0 hours';  -- Accumulates total time worked
    daily_hours INTERVAL;               -- Holds duration for a single day
    work_days INT := 0;                 -- Counter for number of working days
BEGIN
    -- Loop through attendance records for the given employee and month
    FOR rec IN
        SELECT a.check_in_time, a.check_out_time
        FROM attendance_log a
        WHERE a.employee_id = emp_id
          AND EXTRACT(MONTH FROM a.log_date) = month_input
          AND EXTRACT(YEAR FROM a.log_date) = year_input
          AND a.check_in_time IS NOT NULL 
          AND a.check_out_time IS NOT NULL
    LOOP
        -- Calculate duration worked for the current day
        daily_hours := rec.check_out_time - rec.check_in_time;

        -- Add daily hours to total worked hours
        total_hours := total_hours + daily_hours;

        -- Increment working day count
        work_days := work_days + 1;
    END LOOP;

    -- Return the report: employee ID, total days worked, total hours, and average hours per day
    RETURN QUERY
    SELECT emp_id, work_days, total_hours,
           CASE 
               WHEN work_days = 0 THEN NULL           -- Avoid division by zero
               ELSE total_hours / work_days           -- Calculate average hours per day
           END;
END;
$$ LANGUAGE plpgsql;
