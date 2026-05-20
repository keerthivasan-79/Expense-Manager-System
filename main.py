import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from db import get_connection

selected_id = None

# ---------------- DATABASE ----------------

def load_expenses(month=None):
    tree.delete(*tree.get_children())

    con = get_connection()
    cur = con.cursor()

    if month:
        cur.execute("SELECT * FROM expenses WHERE MONTH(date)=%s", (month,))
    else:
        cur.execute("SELECT * FROM expenses")

    for row in cur.fetchall():
        tree.insert("", "end", values=row)

    con.close()

def add_expense():
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO expenses (title, amount, category, date) VALUES (%s,%s,%s,%s)",
        (title.get(), amount.get(), category.get(), date.get())
    )
    con.commit()
    con.close()
    clear_fields()
    load_expenses()

def update_expense():
    if not selected_id:
        return
    con = get_connection()
    cur = con.cursor()
    cur.execute(
        "UPDATE expenses SET title=%s, amount=%s, category=%s, date=%s WHERE id=%s",
        (title.get(), amount.get(), category.get(), date.get(), selected_id)
    )
    con.commit()
    con.close()
    clear_fields()
    load_expenses()

def delete_expense():
    if not selected_id:
        return
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM expenses WHERE id=%s", (selected_id,))
    con.commit()
    con.close()
    clear_fields()
    load_expenses()

def select_item(event):
    global selected_id
    values = tree.item(tree.focus())["values"]
    if not values:
        return
    selected_id = values[0]

    title.delete(0, tk.END)
    amount.delete(0, tk.END)
    category.delete(0, tk.END)
    date.delete(0, tk.END)

    title.insert(0, values[1])
    amount.insert(0, values[2])
    category.insert(0, values[3])
    date.insert(0, values[4])

def clear_fields():
    global selected_id
    selected_id = None
    title.delete(0, tk.END)
    amount.delete(0, tk.END)
    category.delete(0, tk.END)
    date.delete(0, tk.END)

def show_graph():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cur.fetchall()
    con.close()

    if not data:
        messagebox.showinfo("Info", "No data to show")
        return

    plt.bar([d[0] for d in data], [d[1] for d in data], color="teal")
    plt.title("Expense Summary")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.show()

# ---------------- GUI ----------------

root = tk.Tk()
root.title("Expense Manager")
root.geometry("850x600")
root.configure(bg="#f4f6f8")

style = ttk.Style()
style.theme_use("default")

style.configure(
    "Treeview.Heading",
    background="#1f4e79",
    foreground="white",
    font=("Segoe UI", 10, "bold")
)

style.configure(
    "Treeview",
    rowheight=28,
    font=("Segoe UI", 10)
)

# -------- HEADER --------
tk.Label(
    root,
    text="Expense Manager",
    bg="#1f4e79",
    fg="white",
    font=("Segoe UI", 16, "bold"),
    pady=10
).pack(fill=tk.X)

# -------- FORM --------
form = tk.Frame(root, bg="#f4f6f8")
form.pack(pady=10)

def lbl(text, r, c):
    tk.Label(form, text=text, bg="#f4f6f8", font=("Segoe UI", 10)).grid(row=r, column=c, padx=5, pady=5)

lbl("Title", 0, 0)
title = tk.Entry(form, width=20)
title.grid(row=0, column=1)

lbl("Amount", 0, 2)
amount = tk.Entry(form, width=20)
amount.grid(row=0, column=3)

lbl("Category", 1, 0)
category = tk.Entry(form, width=20)
category.grid(row=1, column=1)

lbl("Date (YYYY-MM-DD)", 1, 2)
date = tk.Entry(form, width=20)
date.grid(row=1, column=3)

# -------- BUTTONS --------
btns = tk.Frame(root, bg="#f4f6f8")
btns.pack()

tk.Button(btns, text="Add", bg="#28a745", fg="white", width=12, command=add_expense).grid(row=0, column=0, padx=5)
tk.Button(btns, text="Update", bg="#007bff", fg="white", width=12, command=update_expense).grid(row=0, column=1, padx=5)
tk.Button(btns, text="Delete", bg="#dc3545", fg="white", width=12, command=delete_expense).grid(row=0, column=2, padx=5)
tk.Button(btns, text="Graph", bg="#17a2b8", fg="white", width=12, command=show_graph).grid(row=0, column=3, padx=5)

# -------- FILTER --------
filter_frame = tk.Frame(root, bg="#f4f6f8")
filter_frame.pack(pady=10)

tk.Label(filter_frame, text="Filter Month (1-12):", bg="#f4f6f8").pack(side=tk.LEFT)
month_entry = tk.Entry(filter_frame, width=5)
month_entry.pack(side=tk.LEFT, padx=5)

tk.Button(filter_frame, text="Apply", command=lambda: load_expenses(month_entry.get())).pack(side=tk.LEFT)
tk.Button(filter_frame, text="Reset", command=lambda: load_expenses()).pack(side=tk.LEFT, padx=5)

# -------- TABLE --------
columns = ("ID", "Title", "Amount", "Category", "Date")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(expand=True, fill="both", padx=10, pady=10)
tree.bind("<ButtonRelease-1>", select_item)

load_expenses()
root.mainloop()
