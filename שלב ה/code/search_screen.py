import tkinter as tk
from tkinter import messagebox, scrolledtext
import psycopg2
from db_config import connect_to_db



def open_search_screen(prev_root):
    prev_root.destroy()

    win = tk.Tk()
    win.title("Search Employees")
    win.geometry("650x450")
    win.configure(bg="#23272e")  # רקע כהה

    title_label = tk.Label(
        win, text="Search Employees", font=("Arial", 18, "bold"),
        bg="#23272e", fg="#f5f6fa"
    )
    title_label.pack(pady=15)

    form_frame = tk.Frame(win, bg="#2c313c", bd=2, relief="groove", highlightbackground="#444950", highlightthickness=1)
    form_frame.pack(pady=10, padx=10, fill="x")

    tk.Label(
        form_frame, text="Name contains:", font=("Arial", 12),
        bg="#2c313c", fg="#f5f6fa"
    ).grid(row=0, column=0, padx=8, pady=8, sticky="e")
    name_entry = tk.Entry(form_frame, font=("Arial", 12), width=18, bd=2, relief="groove",
                          bg="#23272e", fg="#f5f6fa", insertbackground="#f5f6fa")
    name_entry.grid(row=0, column=1, padx=8, pady=8)

    tk.Label(
        form_frame, text="Department ID:", font=("Arial", 12),
        bg="#2c313c", fg="#f5f6fa"
    ).grid(row=0, column=2, padx=8, pady=8, sticky="e")
    dept_entry = tk.Entry(form_frame, font=("Arial", 12), width=10, bd=2, relief="groove",
                          bg="#23272e", fg="#f5f6fa", insertbackground="#f5f6fa")
    dept_entry.grid(row=0, column=3, padx=8, pady=8)

    result_box = scrolledtext.ScrolledText(
        win, height=13, width=75, font=("Consolas", 11), bd=2, relief="groove",
        bg="#181b20", fg="#f5f6fa", insertbackground="#f5f6fa"
    )
    result_box.pack(pady=15, padx=10)

    def perform_search():
        name_val = name_entry.get()
        dept_val = dept_entry.get()

        query = "SELECT emp_id, emp_name, department_id FROM employee WHERE 1=1"
        params = []

        if name_val:
            query += " AND emp_name ILIKE %s"
            params.append(f"%{name_val}%")

        if dept_val:
            query += " AND department_id = %s"
            params.append(dept_val)

        conn = connect_to_db()
        if not conn:
            return

        try:
            cur = conn.cursor()
            cur.execute(query, tuple(params))
            rows = cur.fetchall()
            result_box.delete("1.0", tk.END)
            if rows:
                result_box.insert(tk.END, f"{'ID':<8}{'Name':<30}{'Dept ID':<10}\n")
                result_box.insert(tk.END, "-"*50 + "\n")
                for row in rows:
                    result_box.insert(
                        tk.END, f"{row[0]:<8}{row[1]:<30}{row[2]:<10}\n"
                    )
            else:
                result_box.insert(tk.END, "No results found.")
        except Exception as e:
            messagebox.showerror("Search Error", str(e))
        finally:
            conn.close()

    btn_frame = tk.Frame(win, bg="#23272e")
    btn_frame.pack(pady=5)

    search_btn = tk.Button(
        btn_frame, text="Search", command=perform_search,
        font=("Arial", 12, "bold"), bg="#3b82f6", fg="#f5f6fa",
        activebackground="#2563eb", activeforeground="#f5f6fa", width=12, bd=0, cursor="hand2"
    )
    search_btn.grid(row=0, column=0, padx=10)

    back_btn = tk.Button(
        btn_frame, text="Back to Menu", command=lambda: [win.destroy(), main()],
        font=("Arial", 12, "bold"), bg="#636e72", fg="#f5f6fa",
        activebackground="#2d3436", activeforeground="#f5f6fa", width=12, bd=0, cursor="hand2"
    )
    back_btn.grid(row=0, column=1, padx=10)

def main():
    import main as main_module
    main_module.main()
