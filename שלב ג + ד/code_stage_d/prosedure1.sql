CREATE OR REPLACE PROCEDURE add_order_if_in_stock(
    p_department_id INT,
    p_supplier_id INT,
    p_item_id INT,
    p_amount INT,
    p_receipt_id INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    available_qty INT;
    new_order_id INT;
BEGIN
    -- Check available stock
    SELECT quantity INTO available_qty
    FROM stored_in
    WHERE item_id = p_item_id AND department_id = p_department_id;

    IF available_qty IS NULL OR available_qty < p_amount THEN
        RAISE EXCEPTION 'Not enough stock for item ID % in department ID %', p_item_id, p_department_id;
    END IF;

    -- Generate new order_id
    SELECT COALESCE(MAX(order_id), 0) + 1 INTO new_order_id FROM purchase_order;

    -- Insert into purchase_order
    INSERT INTO purchase_order(order_id, order_date)
    VALUES (new_order_id, CURRENT_DATE);

    -- Insert into ordered
    INSERT INTO ordered(order_id, department_id, supplier_id, item_id, receipt_id, amount)
    VALUES (new_order_id, p_department_id, p_supplier_id, p_item_id, p_receipt_id, p_amount);

    -- Update stock
    UPDATE stored_in
    SET quantity = quantity - p_amount
    WHERE item_id = p_item_id AND department_id = p_department_id;

    -- Show inserted data
    RAISE NOTICE 'Order % added for item %, department %, amount %', new_order_id, p_item_id, p_department_id, p_amount;

    -- Optional: display the inserted order
    -- (this SELECT will show when calling via pgAdmin/psql)
    SELECT * FROM ordered WHERE order_id = new_order_id;

END;
$$;
