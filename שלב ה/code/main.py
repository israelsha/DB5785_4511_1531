import tkinter as tk
from employee_screen import open_employee_screen  
from search_screen import open_search_screen
from attendance_screen import open_attendance_screen
from query_screen import open_query_screen
from plsql_screen import open_plsql_screen
from department_screen import open_department_screen

# --- Colors for dark mode ---
BG_COLOR = "#1e1e1e"
FG_COLOR = "#ffffff"
BTN_BG = "#3c3f41"
BTN_FG = "#ffffff"
BTN_HOVER = "#5c5f61"

def on_enter(e):
    e.widget['background'] = BTN_HOVER

def on_leave(e):
    e.widget['background'] = BTN_BG

def main():
    root = tk.Tk()
    root.title("Employee Management System")
    root.geometry("450x500")
    root.configure(bg=BG_COLOR)

    title = tk.Label(root, text="Main Menu", font=("Helvetica", 20), bg=BG_COLOR, fg=FG_COLOR)
    title.pack(pady=20)

    buttons = [
        ("Manage Employees", lambda: open_employee_screen(root)),
        ("Search Employees", lambda: open_search_screen(root)),
        ("Manage Attendance", lambda: open_attendance_screen(root)),
        ("Manage Departments", lambda: open_department_screen(root)),
        ("Run Queries", lambda: open_query_screen(root)),
        ("Functions & Procedures", lambda: open_plsql_screen(root)),
        ("Exit", root.destroy)
    ]

    for text, cmd in buttons:
        btn = tk.Button(root, text=text, font=("Helvetica", 12), width=25, bg=BTN_BG, fg=BTN_FG, command=cmd, relief=tk.FLAT)
        btn.pack(pady=8)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    root.mainloop()

if __name__ == "__main__":
    main()
