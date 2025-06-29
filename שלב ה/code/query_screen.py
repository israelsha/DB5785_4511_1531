import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk
import psycopg2
from db_config import connect_to_db

def open_query_screen(prev_root):
    prev_root.destroy()
    win = tk.Tk()
    win.title("Reports and Queries")
    win.geometry("1100x650")
    win.configure(bg="#23272e")

    label_style = {"bg": "#23272e", "fg": "#3b82f6", "font": ("Arial", 20, "bold")}
    button_style = {
        "bg": "#3b82f6", "fg": "#f5f6fa", "activebackground": "#2563eb", "activeforeground": "#f5f6fa",
        "font": ("Arial", 12, "bold"), "bd": 0, "cursor": "hand2", "width": 26, "height": 2
    }

    tk.Label(win, text="Reports and Queries", **label_style).pack(pady=15)

    columns = ()
    result_table = ttk.Treeview(win, columns=columns, show='headings')
    result_table.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#181b20",
                    foreground="#f5f6fa",
                    rowheight=28,
                    fieldbackground="#181b20",
                    font=("Arial", 12))
    style.configure("Treeview.Heading",
                    background="#2c313c",
                    foreground="#3b82f6",
                    font=("Arial", 12, "bold"))
    style.map("Treeview",
              background=[('selected', '#007acc')])

    def run_query(query, headers, params=None):
        conn = connect_to_db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute(query, params or ())
            rows = cur.fetchall()
            # Update column headers
            result_table["columns"] = headers
            for col in headers:
                result_table.heading(col, text=col)
                result_table.column(col, width=180, anchor="center")
            result_table.delete(*result_table.get_children())
            for row in rows:
                result_table.insert('', tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Query Failed", str(e))
        finally:
            conn.close()

    btn_frame = tk.Frame(win, bg="#23272e")
    btn_frame.pack(pady=10)

    # עיצוב כפתורים: כל כפתור מקבל צבע רקע משלו, אבל לא מעבירים פעמיים את אותו פרמטר (bg/fg)
    # לכן נשתמש ב-button_style רק לפרמטרים המשותפים, ואת הצבעים נשים ישירות בכפתור

    tk.Button(
        btn_frame, text="Employees with No Attendance",
        bg="#3b82f6", activebackground="#2563eb",
        fg="#f5f6fa", activeforeground="#f5f6fa",
        font=("Arial", 12, "bold"), bd=0, cursor="hand2", width=26, height=2,
        command=lambda: run_query(
            """
            SELECT emp_id, emp_name FROM employee
            WHERE emp_id NOT IN (
                SELECT employee_id FROM attendance_log
            )
            """,
            headers=["emp_id", "emp_name"]
        )
    ).grid(row=0, column=0, padx=8, pady=8)

    tk.Button(
        btn_frame, text="Late Check-ins (after 09:00)",
        bg="#f39c12", activebackground="#e67e22",
        fg="#23272e", activeforeground="#23272e",
        font=("Arial", 12, "bold"), bd=0, cursor="hand2", width=26, height=2,
        command=lambda: run_query(
            """
            SELECT e.emp_id, e.emp_name, a.log_date, a.check_in_time
            FROM attendance_log a
            JOIN employee e ON e.emp_id = a.employee_id
            WHERE a.check_in_time > TIME '09:00'
            """,
            headers=["emp_id", "emp_name", "log_date", "check_in_time"]
        )
    ).grid(row=0, column=1, padx=8, pady=8)

    tk.Button(
        btn_frame, text="Departments with No Items Stored",
        bg="#27ae60", activebackground="#219150",
        fg="#f5f6fa", activeforeground="#f5f6fa",
        font=("Arial", 12, "bold"), bd=0, cursor="hand2", width=26, height=2,
        command=lambda: run_query(
            """
            SELECT d.department_id, d.department_name
            FROM department d
            WHERE d.department_id NOT IN (
                SELECT DISTINCT department_id FROM stored_in
            )
            """,
            headers=["department_id", "department_name"]
        )
    ).grid(row=0, column=2, padx=8, pady=8)

    tk.Button(
        btn_frame, text="Employees Without Contracts",
        bg="#e74c3c", activebackground="#c0392b",
        fg="#f5f6fa", activeforeground="#f5f6fa",
        font=("Arial", 12, "bold"), bd=0, cursor="hand2", width=26, height=2,
        command=lambda: run_query(
            """
            SELECT e.emp_id, e.emp_name FROM employee e
            WHERE e.emp_id NOT IN (
                SELECT emp_id FROM contract
            )
            """,
            headers=["emp_id", "emp_name"]
        )
    ).grid(row=0, column=3, padx=8, pady=8)

    tk.Button(
        win, text="Back to Menu",
        font=("Arial", 12, "bold"), bg="#636e72", fg="#f5f6fa",
        activebackground="#2d3436", activeforeground="#f5f6fa",
        bd=0, cursor="hand2", width=20,
        command=lambda: [win.destroy(), __import__('main').main()]
    ).pack(pady=15)
