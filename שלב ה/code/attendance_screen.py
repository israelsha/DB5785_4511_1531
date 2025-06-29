import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from db_config import connect_to_db


def open_attendance_screen(prev_root):
    prev_root.destroy()

    win = tk.Tk()
    win.title("Attendance Management")
    win.geometry("1100x600")
    win.configure(bg="#23272e")

    tk.Label(
        win, text="Attendance Records", font=("Arial", 18, "bold"),
        bg="#23272e", fg="#f5f6fa"
    ).pack(pady=10)

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

    # Table for attendance records
    columns = ("ID", "Employee ID", "Date", "Time In", "Time Out")
    tree = ttk.Treeview(win, columns=columns, show='headings')
    tree.heading("ID", text="Attendance ID")
    tree.heading("Employee ID", text="Employee ID")
    tree.heading("Date", text="Date")
    tree.heading("Time In", text="Time In")
    tree.heading("Time Out", text="Time Out")
    tree.column("ID", width=100, anchor='center')
    tree.column("Employee ID", width=120, anchor='center')
    tree.column("Date", width=120, anchor='center')
    tree.column("Time In", width=100, anchor='center')
    tree.column("Time Out", width=100, anchor='center')
    tree.pack(pady=5, fill="x", padx=20)

    # Input Frame
    form_frame = tk.Frame(win, bg="#2c313c", bd=2, relief="groove", highlightbackground="#444950", highlightthickness=1)
    form_frame.pack(pady=10, padx=20, fill="x")

    label_style = {"font": ("Arial", 12), "bg": "#2c313c", "fg": "#f5f6fa"}
    entry_style = {"font": ("Arial", 12), "bg": "#23272e", "fg": "#f5f6fa", "insertbackground": "#f5f6fa", "bd": 2, "relief": "groove"}

    tk.Label(form_frame, text="Attendance ID (auto):", **label_style).grid(row=0, column=0, padx=8, pady=8, sticky="e")
    id_entry = tk.Entry(form_frame, **entry_style, width=10)
    id_entry.grid(row=0, column=1, padx=8, pady=8)

    tk.Label(form_frame, text="Employee ID:", **label_style).grid(row=0, column=2, padx=8, pady=8, sticky="e")
    emp_entry = tk.Entry(form_frame, **entry_style, width=12)
    emp_entry.grid(row=0, column=3, padx=8, pady=8)

    tk.Label(form_frame, text="Date (YYYY-MM-DD):", **label_style).grid(row=0, column=4, padx=8, pady=8, sticky="e")
    date_entry = tk.Entry(form_frame, **entry_style, width=12)
    date_entry.grid(row=0, column=5, padx=8, pady=8)

    tk.Label(form_frame, text="Time In (HH:MM):", **label_style).grid(row=1, column=0, padx=8, pady=8, sticky="e")
    in_entry = tk.Entry(form_frame, **entry_style, width=12)
    in_entry.grid(row=1, column=1, padx=8, pady=8)

    tk.Label(form_frame, text="Time Out (HH:MM):", **label_style).grid(row=1, column=2, padx=8, pady=8, sticky="e")
    out_entry = tk.Entry(form_frame, **entry_style, width=12)
    out_entry.grid(row=1, column=3, padx=8, pady=8)

    def load_attendance():
        conn = connect_to_db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT log_id, employee_id, log_date, check_in_time, check_out_time FROM attendance_log ORDER BY log_date DESC;")
            rows = cur.fetchall()
            tree.delete(*tree.get_children())
            for row in rows:
                tree.insert('', 'end', values=row)
            # הצע את ה-ID הבא בשדה (אם ריק)
            if rows:
                cur.execute("SELECT MAX(log_id) FROM attendance_log")
                max_id = cur.fetchone()[0]
                next_id = max_id + 1 if max_id else 1
            else:
                next_id = 1
            if not id_entry.get():
                id_entry.delete(0, tk.END)
                id_entry.insert(0, str(next_id))
        except Exception as e:
            messagebox.showerror("Load Failed", str(e))
        finally:
            conn.close()

    def add_attendance():
        att_id = id_entry.get()
        emp = emp_entry.get()
        date = date_entry.get()
        time_in = in_entry.get()
        time_out = out_entry.get()

        if not att_id or not emp or not date or not time_in or not time_out:
            messagebox.showwarning("Missing Data", "Please fill in all fields.")
            return

        try:
            datetime.strptime(date, '%Y-%m-%d')
            datetime.strptime(time_in, '%H:%M')
            datetime.strptime(time_out, '%H:%M')
        except ValueError:
            messagebox.showerror("Invalid Format", "Check date/time formats.")
            return

        conn = connect_to_db()
        if not conn:
            return

        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO attendance_log (log_id, employee_id, log_date, check_in_time, check_out_time)
                VALUES (%s, %s, %s, %s, %s)
            """, (att_id, emp, date, time_in, time_out))
            conn.commit()
            messagebox.showinfo("Success", "Attendance record added.")
            id_entry.delete(0, tk.END)
            load_attendance()
        except Exception as e:
            messagebox.showerror("Insert Failed", str(e))
        finally:
            conn.close()

    def update_attendance():
        att_id = id_entry.get()
        date = date_entry.get()
        time_in = in_entry.get()
        time_out = out_entry.get()

        if not att_id:
            messagebox.showwarning("Missing ID", "Attendance ID is required.")
            return

        if not date and not time_in and not time_out:
            messagebox.showwarning("Missing Data", "Nothing to update.")
            return

        conn = connect_to_db()
        if not conn:
            return

        try:
            cur = conn.cursor()
            if date:
                cur.execute("UPDATE attendance_log SET log_date = %s WHERE log_id = %s", (date, att_id))
            if time_in:
                cur.execute("UPDATE attendance_log SET check_in_time = %s WHERE log_id = %s", (time_in, att_id))
            if time_out:
                cur.execute("UPDATE attendance_log SET check_out_time = %s WHERE log_id = %s", (time_out, att_id))
            conn.commit()
            messagebox.showinfo("Success", "Attendance record updated.")
            load_attendance()
        except Exception as e:
            messagebox.showerror("Update Failed", str(e))
        finally:
            conn.close()

    def delete_attendance():
        att_id = id_entry.get()
        if not att_id:
            messagebox.showwarning("Missing ID", "Attendance ID is required.")
            return

        conn = connect_to_db()
        if not conn:
            return

        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM attendance_log WHERE log_id = %s", (att_id,))
            if cur.rowcount == 0:
                messagebox.showinfo("Not Found", "No record with that ID.")
            else:
                conn.commit()
                messagebox.showinfo("Success", "Record deleted.")
                load_attendance()
        except Exception as e:
            messagebox.showerror("Delete Failed", str(e))
        finally:
            conn.close()

    # Buttons Frame
    btn_frame = tk.Frame(win, bg="#23272e")
    btn_frame.pack(pady=10)

    tk.Button(
        btn_frame, text="Load", command=load_attendance, width=12,
        font=("Arial", 12, "bold"), bg="#3b82f6", fg="#f5f6fa",
        activebackground="#2563eb", activeforeground="#f5f6fa", bd=0, cursor="hand2"
    ).grid(row=0, column=0, padx=8)
    tk.Button(
        btn_frame, text="Add", command=add_attendance, width=12,
        font=("Arial", 12, "bold"), bg="#27ae60", fg="#f5f6fa",
        activebackground="#219150", activeforeground="#f5f6fa", bd=0, cursor="hand2"
    ).grid(row=0, column=1, padx=8)
    tk.Button(
        btn_frame, text="Update", command=update_attendance, width=12,
        font=("Arial", 12, "bold"), bg="#f39c12", fg="#23272e",
        activebackground="#e67e22", activeforeground="#23272e", bd=0, cursor="hand2"
    ).grid(row=0, column=2, padx=8)
    tk.Button(
        btn_frame, text="Delete", command=delete_attendance, width=12,
        font=("Arial", 12, "bold"), bg="#e74c3c", fg="#f5f6fa",
        activebackground="#c0392b", activeforeground="#f5f6fa", bd=0, cursor="hand2"
    ).grid(row=0, column=3, padx=8)
    tk.Button(
        btn_frame, text="Back to Menu", command=lambda: [win.destroy(), main()], width=12,
        font=("Arial", 12, "bold"), bg="#636e72", fg="#f5f6fa",
        activebackground="#2d3436", activeforeground="#f5f6fa", bd=0, cursor="hand2"
    ).grid(row=0, column=4, padx=8)

    # טען את ה-ID הבא כבר בפתיחה
    load_attendance()

def main():
    import main as main_module
    main_module.main()
