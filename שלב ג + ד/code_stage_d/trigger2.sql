CREATE OR REPLACE FUNCTION validate_attendance_times()
RETURNS TRIGGER AS $$
BEGIN
-- If the exit time is earlier than the entry time - throw an error
    IF NEW.check_out_time < NEW.check_in_time THEN
        RAISE EXCEPTION 'Invalid attendance log: check-out time (%, employee_id=%) is earlier than check-in time (%).',
            NEW.check_out_time, NEW.employee_id, NEW.check_in_time;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_validate_attendance_times ON attendance_log;

CREATE TRIGGER trg_validate_attendance_times
BEFORE INSERT OR UPDATE ON attendance_log
FOR EACH ROW
EXECUTE FUNCTION validate_attendance_times();
