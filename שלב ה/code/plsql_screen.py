import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
import psycopg2
from db_config import connect_to_db


def open_plsql_screen(prev_root):
    prev_root.destroy()
    win = tk.Tk()
    win.title("Functions & Procedures")
    win.geometry("1200x900")
    win.configure(bg="#23272e")

    tk.Label(win, text="Functions & Procedures", font=("Arial", 20, "bold"), bg="#23272e", fg="#3b82f6").pack(pady=15)

    output = scrolledtext.ScrolledText(
        win, height=12, width=140, font=("Consolas", 12),
        bg="#181b20", fg="#f5f6fa", insertbackground="#f5f6fa", bd=2, relief="groove"
    )
    output.pack(pady=10, padx=20)

    # --- Function 1: Monthly Report ---
    frame1 = tk.LabelFrame(win, text="Get Employee Monthly Report", padx=10, pady=5,
                           bg="#2c313c", fg="#3b82f6", font=("Arial", 13, "bold"), bd=2, relief="groove", highlightbackground="#444950", highlightthickness=1)
    frame1.pack(padx=20, pady=8, fill="x")
    for widget in frame1.winfo_children():
        widget.configure(bg="#2c313c", fg="#f5f6fa", font=("Arial", 12))
    tk.Label(frame1, text="Emp ID", bg="#2c313c", fg="#f5f6fa", font=("Arial", 12)).grid(row=0, column=0, padx=8, pady=8, sticky="e")
    emp_id_entry = tk.Entry(frame1, bg="#23272e", fg="#f5f6fa", insertbackground="#f5f6fa", font=("Arial", 12), bd=2, relief="groove", width=10)
    emp_id_entry.grid(row=0, column=1, padx=8, pady=8)
    tk.Label(frame1, text="Month", bg="#2c313c", fg="#f5f6fa", font=("Arial", 12)).grid(row=0, column=2, padx=8, pady=8, sticky="e")
    month_entry = tk.Entry(frame1, bg="#23272e", fg="#f5f6fa", insertbackground="#f5f6fa", font=("Arial", 12), bd=2, relief="groove", width=10)
    month_entry.grid(row=0, column=3, padx=8, pady=8)
    tk.Label(frame1, text="Year", bg="#2c313c", fg="#f5f6fa", font=("Arial", 12)).grid(row=0, column=4, padx=8, pady=8, sticky="e")
    year_entry = tk.Entry(frame1, bg="#23272e", fg="#f5f6fa", insertbackground="#f5f6fa", font=("Arial", 12), bd=2, relief="groove", width=10)
    year_entry.grid(row=0, column=5, padx=8, pady=8)
    tk.Button(frame1, text="Run", bg="#3b82f6", fg="#f5f6fa", activebackground="#2563eb", activeforeground="#f5f6fa",
              font=("Arial", 12, "bold"), bd=0, cursor="hand2", width=10,
              command=lambda: run_function_1(emp_id_entry.get(), month_entry.get(), year_entry.get())
    ).grid(row=0, column=6, padx=12, pady=8)

    # --- Function 2: Price Gap Report ---
    frame2 = tk.LabelFrame(win, text="Report Price Gap Between Suppliers", padx=10, pady=5,
                           bg="#2c313c", fg="#3b82f6", font=("Arial", 13, "bold"), bd=2, relief="groove", highlightbackground="#444950", highlightthickness=1)
    frame2.pack(padx=20, pady=8, fill="x")
    tk.Label(frame2, text="Item Limit", bg="#2c313c", fg="#f5f6fa", font=("Arial", 12)).grid(row=0, column=0, padx=8, pady=8, sticky="e")
    item_limit_entry = tk.Entry(frame2, bg="#23272e", fg="#f5f6fa", insertbackground="#f5f6fa", font=("Arial", 12), bd=2, relief="groove", width=10)
    item_limit_entry.grid(row=0, column=1, padx=8, pady=8)
    tk.Button(frame2, text="Run", bg="#27ae60", fg="#f5f6fa", activebackground="#219150", activeforeground="#f5f6fa",
              font=("Arial", 12, "bold"), bd=0, cursor="hand2", width=10,
              command=lambda: run_function_2(item_limit_entry.get())
    ).grid(row=0, column=2, padx=12, pady=8)

    # --- Procedure 1: Add Order if In Stock ---
    frame3 = tk.LabelFrame(win, text="Add Order If In Stock", padx=10, pady=5,
                           bg="#2c313c", fg="#3b82f6", font=("Arial", 13, "bold"), bd=2, relief="groove", highlightbackground="#444950", highlightthickness=1)
    frame3.pack(padx=20, pady=8, fill="x")
    labels = ["Dept ID", "Supplier ID", "Item ID", "Amount", "Receipt ID"]
    proc1_entries = []
    for i, label in enumerate(labels):
        tk.Label(frame3, text=label, bg="#2c313c", fg="#f5f6fa", font=("Arial", 12)).grid(row=0, column=i*2, padx=8, pady=8, sticky="e")
        e = tk.Entry(frame3, bg="#23272e", fg="#f5f6fa", insertbackground="#f5f6fa", font=("Arial", 12), bd=2, relief="groove", width=10)
        e.grid(row=0, column=i*2 + 1, padx=8, pady=8)
        proc1_entries.append(e)
    tk.Button(frame3, text="Run", bg="#f39c12", fg="#23272e", activebackground="#e67e22", activeforeground="#23272e",
              font=("Arial", 12, "bold"), bd=0, cursor="hand2", width=10,
              command=lambda: run_proc_1([int(e.get()) for e in proc1_entries])
    ).grid(row=0, column=10, padx=24, pady=8, sticky="e")  # הגדל padx ו-sticky לימין

    # --- Procedure 2: Update Prices By Percent ---
    frame4 = tk.LabelFrame(win, text="Update Prices By Percent", padx=10, pady=5,
                           bg="#2c313c", fg="#3b82f6", font=("Arial", 13, "bold"), bd=2, relief="groove", highlightbackground="#444950", highlightthickness=1)
    frame4.pack(padx=20, pady=8, fill="x")
    tk.Label(frame4, text="Percent Change", bg="#2c313c", fg="#f5f6fa", font=("Arial", 12)).grid(row=0, column=0, padx=8, pady=8, sticky="e")
    percent_entry = tk.Entry(frame4, bg="#23272e", fg="#f5f6fa", insertbackground="#f5f6fa", font=("Arial", 12), bd=2, relief="groove", width=10)
    percent_entry.grid(row=0, column=1, padx=8, pady=8)
    tk.Button(frame4, text="Run", bg="#e74c3c", fg="#f5f6fa", activebackground="#c0392b", activeforeground="#f5f6fa",
              font=("Arial", 12, "bold"), bd=0, cursor="hand2", width=10,
              command=lambda: run_proc_2(percent_entry.get())
    ).grid(row=0, column=2, padx=12, pady=8)

    # מקם את כפתור Back to Menu בתחתית החלון, תמיד ייראה
    btn_back = tk.Button(
        win, text="Back to Menu",
        command=lambda: [win.destroy(), __import__('main').main()],
        font=("Arial", 12, "bold"), bg="#636e72", fg="#f5f6fa",
        activebackground="#2d3436", activeforeground="#f5f6fa",
        bd=0, cursor="hand2", width=20
    )
    btn_back.place(relx=0.5, rely=0.98, anchor="s")  # ממורכז בתחתית

    def run_function_1(emp_id, month, year):
        conn = connect_to_db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM get_employee_monthly_report(%s, %s, %s);", (emp_id, month, year))
            rows = cur.fetchall()
            output.delete("1.0", tk.END)
            if rows:
                col_names = [desc[0] for desc in cur.description]
                header = " | ".join(f"{col:<18}" for col in col_names)
                output.insert(tk.END, header + "\n")
                output.insert(tk.END, "-" * len(header) + "\n")
                for row in rows:
                    line = " | ".join(f"{str(val):<18}" for val in row)
                    output.insert(tk.END, line + "\n")
            else:
                output.insert(tk.END, "No results found.")
        except Exception as e:
            messagebox.showerror("Function Failed", str(e))
        finally:
            conn.close()

    def run_function_2(item_limit):
        conn = connect_to_db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM report_price_gap_between_suppliers(%s);", (item_limit,))
            rows = cur.fetchall()
            output.delete("1.0", tk.END)
            if rows:
                col_names = [desc[0] for desc in cur.description]
                header = " | ".join(f"{col:<18}" for col in col_names)
                output.insert(tk.END, header + "\n")
                output.insert(tk.END, "-" * len(header) + "\n")
                for row in rows:
                    line = " | ".join(f"{str(val):<18}" for val in row)
                    output.insert(tk.END, line + "\n")
            else:
                output.insert(tk.END, "No results found.")
        except Exception as e:
            messagebox.showerror("Function Failed", str(e))
        finally:
            conn.close()

    def run_proc_1(params):
        conn = connect_to_db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("CALL add_order_if_in_stock(%s, %s, %s, %s, %s);", params)
            conn.commit()
            messagebox.showinfo("Success", "Order added successfully.")
        except Exception as e:
            messagebox.showerror("Procedure Failed", str(e))
        finally:
            conn.close()

    def run_proc_2(percent):
        conn = connect_to_db()
        if not conn:
            return
        try:
            cur = conn.cursor()
            cur.execute("CALL update_prices_by_percent(%s);", (percent,))
            conn.commit()
            messagebox.showinfo("Success", "Prices updated successfully.")
        except Exception as e:
            messagebox.showerror("Procedure Failed", str(e))
        finally:
            conn.close()