import tkinter as tk
from tkinter import messagebox
import psycopg2
from db_config import connect_to_db

def open_department_screen(prev_root):
    prev_root.destroy()
    win = tk.Tk()
    win.title("Department Management")
    win.geometry("1100x600")
    win.configure(bg="#23272e")

    # Title
    tk.Label(win, text="Department Management", font=("Arial", 22, "bold"), bg="#23272e", fg="#f5f6fa").pack(pady=(10, 0))

    # Result display at the top
    result = tk.Text(win, height=12, width=120, bg="#181b20", fg="#f5f6fa", insertbackground="#f5f6fa", font=("Consolas", 11), bd=2, relief="groove")
    result.pack(pady=(15, 10), padx=20)

    # Input Frame (like attendance)
    form_frame = tk.Frame(win, bg="#2c313c", bd=2, relief="groove", highlightbackground="#444950", highlightthickness=1)
    form_frame.pack(pady=5, padx=20, fill="x")

    label_style = {"bg": "#2c313c", "fg": "#f5f6fa", "font": ("Arial", 12)}
    entry_style = {"bg": "#23272e", "fg": "#f5f6fa", "insertbackground": "#f5f6fa", "font": ("Arial", 12), "bd": 2, "relief": "groove"}

    # Row 1
    tk.Label(form_frame, text="Department ID (auto):", **label_style).grid(row=0, column=0, padx=8, pady=8, sticky="e")
    id_entry = tk.Entry(form_frame, **entry_style, width=15)
    id_entry.grid(row=0, column=1, padx=8, pady=8)

    tk.Label(form_frame, text="Location:", **label_style).grid(row=0, column=2, padx=8, pady=8, sticky="e")
    location_entry = tk.Entry(form_frame, **entry_style, width=15)
    location_entry.grid(row=0, column=3, padx=8, pady=8)

    # Row 2
    tk.Label(form_frame, text="Department Name:", **label_style).grid(row=1, column=0, padx=8, pady=8, sticky="e")
    name_entry = tk.Entry(form_frame, **entry_style, width=15)
    name_entry.grid(row=1, column=1, padx=8, pady=8)

    tk.Label(form_frame, text="Head of Department:", **label_style).grid(row=1, column=2, padx=8, pady=8, sticky="e")
    head_entry = tk.Entry(form_frame, **entry_style, width=15)
    head_entry.grid(row=1, column=3, padx=8, pady=8)

    # Buttons Frame (like attendance)
    btn_frame = tk.Frame(win, bg="#23272e")
    btn_frame.pack(pady=15)

    tk.Button(btn_frame, text="Load", command=lambda: load_departments(),
              bg="#3b82f6", fg="#f5f6fa", activebackground="#2563eb", activeforeground="#f5f6fa",
              font=("Arial", 12, "bold"), bd=0, cursor="hand2", width=12).grid(row=0, column=0, padx=8)
    tk.Button(btn_frame, text="Add", command=lambda: add_department(),
              bg="#27ae60", fg="#f5f6fa", activebackground="#219150", activeforeground="#f5f6fa",
              font=("Arial", 12, "bold"), bd=0, cursor="hand2", width=12).grid(row=0, column=1, padx=8)
    tk.Button(btn_frame, text="Update", command=lambda: update_department(),
              bg="#f39c12", fg="#23272e", activebackground="#e67e22", activeforeground="#23272e",
              font=("Arial", 12, "bold"), bd=0, cursor="hand2", width=12).grid(row=0, column=2, padx=8)
    tk.Button(btn_frame, text="Delete", command=lambda: delete_department(),
              bg="#e74c3c", fg="#f5f6fa", activebackground="#c0392b", activeforeground="#f5f6fa",
              font=("Arial", 12, "bold"), bd=0, cursor="hand2", width=12).grid(row=0, column=3, padx=8)
    tk.Button(btn_frame, text="Back to Menu", command=lambda: [win.destroy(), __import__('main').main()],
              bg="#636e72", fg="#f5f6fa", activebackground="#2d3436", activeforeground="#f5f6fa",
              font=("Arial", 12, "bold"), bd=0, cursor="hand2", width=14).grid(row=0, column=4, padx=8)

    def load_departments():
        conn = connect_to_db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM department ORDER BY department_id")
            rows = cur.fetchall()
            result.delete("1.0", tk.END)
            if rows:
                result.insert(tk.END, f"{'ID':<8}{'Location':<20}{'Name':<25}{'Head':<20}\n")
                result.insert(tk.END, "-"*75 + "\n")
                for row in rows:
                    result.insert(tk.END, f"{row[0]:<8}{row[1]:<20}{row[2]:<25}{row[3]:<20}\n")
                next_id = rows[-1][0] + 1
            else:
                result.insert(tk.END, "No departments found.\n")
                next_id = 1
            # אל תמלא אוטומטית את השדה, רק אם הוא ריק
            if not id_entry.get():
                id_entry.delete(0, tk.END)
                id_entry.insert(0, str(next_id))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def add_department():
        dep_id = id_entry.get()
        location = location_entry.get()
        name = name_entry.get()
        head = head_entry.get()
        if not (dep_id and location and name and head):
            messagebox.showerror("Error", "All fields must be filled")
            return
        conn = connect_to_db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO department(department_id, location, department_name, head_of_department) VALUES (%s, %s, %s, %s)",
                        (dep_id, location, name, head))
            conn.commit()
            messagebox.showinfo("Success", "Department added successfully.")
            # נקה את השדה כדי שיתמלא אוטומטית בפעם הבאה
            id_entry.delete(0, tk.END)
            load_departments()
        except Exception as e:
            messagebox.showerror("Insert Failed", str(e))
        finally:
            conn.close()

    def delete_department():
        dep_id = id_entry.get()
        if not dep_id:
            messagebox.showerror("Error", "Department ID is required")
            return
        conn = connect_to_db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM department WHERE department_id = %s", (dep_id,))
            if cur.rowcount == 0:
                messagebox.showinfo("Not Found", "No department with that ID.")
            else:
                conn.commit()
                messagebox.showinfo("Success", "Department deleted successfully.")
                load_departments()
        except Exception as e:
            messagebox.showerror("Delete Failed", str(e))
        finally:
            conn.close()

    def update_department():
        dep_id = id_entry.get()
        location = location_entry.get()
        name = name_entry.get()
        head = head_entry.get()
        if not dep_id:
            messagebox.showerror("Error", "Department ID is required for update")
            return
        conn = connect_to_db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE department SET location=%s, department_name=%s, head_of_department=%s WHERE department_id=%s",
                (location, name, head, dep_id)
            )
            if cur.rowcount == 0:
                messagebox.showinfo("Not Found", "No department with that ID.")
            else:
                conn.commit()
                messagebox.showinfo("Success", "Department updated successfully.")
                load_departments()
        except Exception as e:
            messagebox.showerror("Update Failed", str(e))
        finally:
            conn.close()

    # טען את ה-ID הבא כבר בפתיחה
    load_departments()

    win.mainloop()
