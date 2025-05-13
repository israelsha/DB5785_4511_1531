CREATE TABLE Employee (
    Emp_ID SERIAL PRIMARY KEY,
    Emp_Name VARCHAR(255),
    Department_ID INT,
    Position_id INT
);

CREATE TABLE Contract (
    Contract_ID SERIAL PRIMARY KEY,
    Emp_ID INT,
    Start_Date DATE,
    End_Date DATE,
    Salary NUMERIC(10, 2),
    FOREIGN KEY (Emp_ID) REFERENCES Employee(Emp_ID)
);

CREATE TABLE Attendance_Log (
    log_id SERIAL PRIMARY KEY,
    employee_id INT,
    log_date DATE,
    check_in_time TIME,
    check_out_time TIME,
    FOREIGN KEY (employee_id) REFERENCES Employee(Emp_ID)
);

CREATE TABLE Leave_Requests (
    Leave_ID SERIAL PRIMARY KEY,
    Emp_ID INT,
    Start_Date DATE,
    End_Date DATE,
    Status VARCHAR(50),
    FOREIGN KEY (Emp_ID) REFERENCES Employee(Emp_ID)
);

CREATE TABLE Position (
    position_id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    level INT
);

CREATE TABLE EntityDepartment (
    department_id SERIAL PRIMARY KEY,
    location VARCHAR(255),
    name VARCHAR(255)
);
