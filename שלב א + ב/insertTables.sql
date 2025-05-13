-- Insert into Employee
INSERT INTO Employee (Emp_Name, Department_ID, Position_id) VALUES 
('David Cohen', 1, 1),
('Sarah Levi', 2, 2),
('Moshe Mizrahi', 1, 2),
('Dana Avraham', 2, 3);

-- Insert into Position
INSERT INTO Position (title, level) VALUES 
('Manager', 5),
('Developer', 3),
('Analyst', 2);

-- Insert into EntityDepartment
INSERT INTO EntityDepartment (location, name) VALUES 
('Tel Aviv', 'IT'),
('Jerusalem', 'Finance'),
('Haifa', 'HR');

-- Insert into Contract
INSERT INTO Contract (Emp_ID, Start_Date, End_Date, Salary) VALUES 
(1, '2022-01-01', '2024-01-01', 15000.00),
(2, '2021-06-01', '2023-06-01', 12000.00),
(3, '2023-03-01', '2025-03-01', 13000.00);

-- Insert into Attendance_Log
INSERT INTO Attendance_Log (employee_id, log_date, check_in_time, check_out_time) VALUES 
(1, '2024-04-28', '08:00', '17:00'),
(2, '2024-04-28', '08:30', '17:30'),
(3, '2024-04-28', '09:00', '18:00');

-- Insert into Leave_Requests
INSERT INTO Leave_Requests (Emp_ID, Start_Date, End_Date, Status) VALUES 
(1, '2024-05-01', '2024-05-10', 'Approved'),
(2, '2024-06-01', '2024-06-07', 'Pending'),
(3, '2024-07-15', '2024-07-20', 'Rejected');
