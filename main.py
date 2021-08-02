from database import main
import tkinter as tk
from tkinter import ttk
import database as db

def balance_read_write(type="r", data=None):
    if type=="r":
        with open("log.txt", "r") as f:
            balance = int(f.readline())
            rr = int(f.readline())
            return balance, rr
    elif type=="w":
        if data is not None:
            with open("log.txt", "w") as f:
                f.writeline(data[0])
                f.writeline(data[1])
    

FONT = ("Helvetica", 12)
root = tk.Tk()
root.title("Script Analysis")
root.geometry("700x500")
main_tree = ttk.Treeview(root)
main_tree['columns'] = ("Script", "Lot Size", "Margin", "SL pts.", "TP pts.", "SL amt.", "TP amt.", "RR %")

# Formating columns
main_tree.column("#0", width=0, minwidth = 0)
main_tree.column("Script", width=70, minwidth = 50)
main_tree.column("Lot Size", width=60, minwidth = 50)
main_tree.column("Margin", width=60, minwidth = 50)
main_tree.column("SL pts.", width=60, minwidth = 50)
main_tree.column("TP pts.", width=60, minwidth = 50)
main_tree.column("SL amt.", width=60, minwidth = 50)
main_tree.column("TP amt.", width=60, minwidth = 50)
main_tree.column("RR %", width=60, minwidth = 50)

# formatting Headers
main_tree.heading("#0", text="")
main_tree.heading("Script", text="Script")
main_tree.heading("Lot Size", text="Lot Size")
main_tree.heading("Margin", text="Margin")
main_tree.heading("SL pts.", text="SL Pts.")
main_tree.heading("TP pts.", text="TP Pts.")
main_tree.heading("SL amt.", text="SL Amt.")
main_tree.heading("TP amt.", text="TP Amt.")
main_tree.heading("RR %", text="RR %")

script_var = tk.StringVar(root, value="script")
sl_var = tk.StringVar(root, value="SL in pts.")

script_search = tk.Entry(root, textvariable=script_var, width=10, font=FONT)
sl_entry = tk.Entry(root, textvariable=sl_var, width=10, font=FONT)



script_search.place(x=10, y=10)
sl_entry.place(x=130, y=10)

main_tree.place(x=10, y=50)

def calc_row():


def insert_script():
    script_name = script_search.get()
    sl_value = sl_entry.get()


insert_button = tk.Button(root, text="Insert", command=insert_script)



root.mainloop()