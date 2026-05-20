from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
import backend_db

root = Tk()
root.title("Monthly Expense Tracker")
root.geometry("420x400")


def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    note = note_entry.get()

    if date == "" or category == "" or amount == "":
        messagebox.showerror("Error", "Please fill all required fields")
        return

    backend_db.add_expense(date, category, float(amount), note)
    messagebox.showinfo("Success", "Expense Added")

    date_entry.delete(0, END)
    category_entry.delete(0, END)
    amount_entry.delete(0, END)
    note_entry.delete(0, END)

def show_graph():
    data = backend_db.get_monthly_expenses()

    if not data:
        messagebox.showerror("No Data", "No expenses found")
        return

    months = [row[0] for row in data]
    amounts = [row[1] for row in data]

    plt.figure()
    plt.bar(months, amounts)
    plt.xlabel("Month")
    plt.ylabel("Total Expense")
    plt.title("Monthly Expense Graph")
    plt.show()


Label(root, text="Expense Tracker", font=("Arial", 18, "bold")).pack(pady=10)

Label(root, text="Date (YYYY-MM-DD)").pack()
date_entry = Entry(root)
date_entry.pack()

Label(root, text="Category").pack()
category_entry = Entry(root)
category_entry.pack()

Label(root, text="Amount").pack()
amount_entry = Entry(root)
amount_entry.pack()

Label(root, text="Note").pack()
note_entry = Entry(root)
note_entry.pack()

Button(root, text="Add Expense", width=20, command=add_expense).pack(pady=10)
Button(root, text="Show Monthly Graph", width=20, command=show_graph).pack()

root.mainloop()
