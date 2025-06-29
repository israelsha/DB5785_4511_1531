import tkinter as tk
from tkinter import messagebox, ttk
from db_config import connect_to_db

def open_employee_screen(prev_root):
    prev_root.destroy()

    win = tk.Tk()
    win.title("Employee Management")
    win.geometry("900x600")
    win.configure(bg="#23272e")  # רקע כהה

    label_style = {"bg": "#23272e", "fg": "#f5f6fa", "font": ("Arial", 12)}
    entry_style = {"bg": "#181b20", "fg": "#f5f6fa", "insertbackground": "#f5f6fa", "font": ("Arial", 12), "bd": 2, "relief": "groove"}
    button_common = {"font": ("Arial", 12, "bold"), "fg": "#f5f6fa", "bd": 0, "cursor": "hand2"}

    tk.Label(win, text="Employee Management", font=("Arial", 18, "bold"), bg="#23272e", fg="#3b82f6").pack(pady=15)

    # Table style setup
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#181b20",
                    foreground="#f5f6fa",
                    rowheight=25,
                    fieldbackground="#181b20",
                    bordercolor="#444950",
                    borderwidth=1)
    style.configure("Treeview.Heading",
                    background="#2c313c",
                    foreground="#3b82f6",
                    font=("Arial", 11, "bold"))

    tree = ttk.Treeview(win, columns=("ID", "Name", "Department"), show='headings')
    tree.heading("ID", text="Emp ID")
    tree.heading("Name", text="Employee Name")
    tree.heading("Department", text="Department ID")
    tree.column("ID", width=80, anchor='center')
    tree.column("Name", width=200, anchor='center')
    tree.column("Department", width=120, anchor='center')
    tree.pack(pady=5, fill="x", padx=20)

    # Entry fields - single row like attendance
    entry_frame = tk.Frame(win, bg="#2c313c", bd=2, relief="groove", highlightbackground="#444950", highlightthickness=1)
    entry_frame.pack(pady=10, padx=10, fill="x")

    tk.Label(entry_frame, text="Emp ID (auto):", **label_style).grid(row=0, column=0, padx=8, pady=8, sticky="e")
    id_entry = tk.Entry(entry_frame, **entry_style, width=10)
    id_entry.grid(row=0, column=1, padx=8, pady=8)

    tk.Label(entry_frame, text="Name:", **label_style).grid(row=0, column=2, padx=8, pady=8, sticky="e")
    name_entry = tk.Entry(entry_frame, **entry_style, width=18)
    name_entry.grid(row=0, column=3, padx=8, pady=8)

    tk.Label(entry_frame, text="Department ID:", **label_style).grid(row=0, column=4, padx=8, pady=8, sticky="e")
    dept_entry = tk.Entry(entry_frame, **entry_style, width=18)
    dept_entry.grid(row=0, column=5, padx=8, pady=8)

    # Buttons
    btn_frame = tk.Frame(win, bg="#23272e")
    btn_frame.pack(pady=15)

    tk.Button(btn_frame, text="Load Employees", command=lambda: load_employees(tree, id_entry),
              bg="#3b82f6", activebackground="#2563eb", **button_common, width=15).grid(row=0, column=0, padx=8)
    tk.Button(btn_frame, text="Add Employee", command=lambda: add_employee(id_entry, name_entry, dept_entry, tree),
              bg="#27ae60", activebackground="#219150", **button_common, width=15).grid(row=0, column=1, padx=8)
    tk.Button(btn_frame, text="Delete Employee", command=lambda: delete_employee(id_entry, tree),
              bg="#e74c3c", activebackground="#c0392b", **button_common, width=15).grid(row=0, column=2, padx=8)
    tk.Button(btn_frame, text="Update Employee", command=lambda: update_employee(id_entry, name_entry, dept_entry, tree),
              bg="#f39c12", fg="#23272e", activebackground="#e67e22", activeforeground="#23272e", font=("Arial", 12, "bold"), bd=0, cursor="hand2", width=15).grid(row=0, column=3, padx=8)
    tk.Button(btn_frame, text="Back to Menu", command=lambda: [win.destroy(), main()],
              bg="#636e72", activebackground="#2d3436", **button_common, width=15).grid(row=0, column=4, padx=8)

    load_employees(tree, id_entry)

def load_employees(tree, id_entry):
    conn = connect_to_db()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT emp_id, emp_name, department_id FROM employee")
        rows = cur.fetchall()
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert('', 'end', values=row)
        # הצע את ה-ID הבא בשדה (אם ריק)
        if rows:
            next_id = max(row[0] for row in rows) + 1
        else:
            next_id = 1
        if not id_entry.get():
            id_entry.delete(0, tk.END)
            id_entry.insert(0, str(next_id))
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

def add_employee(id_entry, name_entry, dept_entry, tree):
    emp_id = id_entry.get()
    name = name_entry.get()
    dept = dept_entry.get()
    if not emp_id or not name or not dept:
        messagebox.showwarning("Input Error", "All fields are required.")
        return
    conn = connect_to_db()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO employee (emp_id, emp_name, department_id) VALUES (%s, %s, %s)", (emp_id, name, dept))
        conn.commit()
        messagebox.showinfo("Success", f"Employee '{name}' added.")
        # נקה את השדה כדי שיתמלא אוטומטית בפעם הבאה
        id_entry.delete(0, tk.END)
        load_employees(tree, id_entry)
    except Exception as e:
        messagebox.showerror("Insert Failed", str(e))
    finally:
        conn.close()

def delete_employee(id_entry, tree):
    emp_id = id_entry.get()
    if not emp_id:
        messagebox.showwarning("Input Error", "Employee ID is required.")
        return
    conn = connect_to_db()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM employee WHERE emp_id = %s", (emp_id,))
        if cur.rowcount == 0:
            messagebox.showwarning("Not Found", "No employee with that ID.")
        else:
            conn.commit()
            messagebox.showinfo("Deleted", "Employee deleted.")
            load_employees(tree, id_entry)  # <-- תקן כאן
    except Exception as e:
        messagebox.showerror("Delete Failed", str(e))
    finally:
        conn.close()

def update_employee(id_entry, name_entry, dept_entry, tree):
    emp_id = id_entry.get()
    new_name = name_entry.get()
    new_dept = dept_entry.get()
    if not emp_id or not new_name or not new_dept:
        messagebox.showwarning("Input Error", "All fields are required.")
        return
    conn = connect_to_db()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("UPDATE employee SET emp_name = %s, department_id = %s WHERE emp_id = %s",
                    (new_name, new_dept, emp_id))
        if cur.rowcount == 0:
            messagebox.showwarning("Not Found", "No employee with that ID.")
        else:
            conn.commit()
            messagebox.showinfo("Success", "Employee updated.")
            load_employees(tree, id_entry)  
    except Exception as e:
        messagebox.showerror("Update Failed", str(e))
    finally:
        conn.close()

def main():
    import main
    main.main()
