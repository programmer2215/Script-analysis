from database import main
import tkinter as tk
from tkinter import ttk
import database as db    


def read_write(type="r", data=None):
    if type=="r":
        with open("log.txt", "r") as f:
            balance = int(f.readline())
            rr = int(f.readline())
            return balance, rr
    elif type=="w":
        if data is not None:
            with open("log.txt", "w") as f:
                f.write(data[0] + "\n")
                f.write(data[1])
    

FONT = ("Helvetica", 12)
root = tk.Tk()
root.title("Script Analysis")
root.geometry("700x500")

style = ttk.Style()
style.configure("Treeview",
    background="silver",
    foreground="black",
    rowheight=25,
    fieldbackground="silver",
    font=FONT
)
style.configure("Treeview.Heading", font=FONT)
style.map('Treeview', background=[('selected', 'green')]
)

main_tree = ttk.Treeview(root)

main_tree['columns'] = ("Script", "Lot Size", "Margin", "SL pts.", "TP pts.", "SL amt.", "TP amt.", "RR %")

# Formating columns
main_tree.column("#0", width=0, minwidth = 0)
main_tree.column("Script", width=90, minwidth = 50)
main_tree.column("Lot Size", width=70, minwidth = 50)
main_tree.column("Margin", width=80, minwidth = 50)
main_tree.column("SL pts.", width=70, minwidth = 50)
main_tree.column("TP pts.", width=70, minwidth = 50)
main_tree.column("SL amt.", width=70, minwidth = 50)
main_tree.column("TP amt.", width=70, minwidth = 50)
main_tree.column("RR %", width=90, minwidth = 50)

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

main_tree.tag_configure(tagname="green", background="#4feb34")
main_tree.tag_configure(tagname="orange", background="#eb8f34")
main_tree.tag_configure(tagname="red", background="#f03329")

#summary_tree = ttk.Treeview(root)
#summary_tree['columns'] = ('tot. loss', 'tot. profit', 'tot. rr%', 'tot. margin')



script_var = tk.StringVar(root, value="script")
sl_var = tk.StringVar(root, value="SL in pts.")
rr_var = tk.StringVar(root, value=read_write()[1])
balance_var = tk.StringVar(root, value=read_write()[0])

options = tuple(db.get_script_options())
script_search = ttk.Combobox(root, textvariable=script_var, width=10, font=FONT)
script_search['values'] = options
script_search['state'] = 'readonly'
script_search.pack()
sl_entry = tk.Entry(root, textvariable=sl_var, width=10, font=FONT)
rr_entry = tk.Entry(root, textvariable=rr_var, width=10, font=FONT)
balance_entry = tk.Entry(root, textvariable=balance_var, width=10, font=FONT)


script_search.place(x=10, y=20)
sl_entry.place(x=130, y=20)
rr_entry.place(x = 250, y = 20)
balance_entry.place(x=370, y=20)

main_tree.place(x=10, y=50)

def rr_highlight_color(value):
    if value <= 1.0:
        return "green"
    elif value >1.0 and value <=3.0:
        return "orange"
    elif value > 3.0:
        return "red"
    return None


def insert_script():
    balance = balance_entry.get()
    rr = rr_entry.get()
    if read_write() != (balance, rr):
        read_write('w', (balance, rr))
    
    script_name = script_search.get()
    sl_value = int(sl_entry.get())
    data = db.get_row(script_name, sl_value, *read_write())
    tag_val = rr_highlight_color(float(data[-1]))
    main_tree.insert('', 'end', values=data, tag=tag_val)


insert_button = tk.Button(root, text="Insert", command=insert_script)
insert_button.place(x =470, y=10)


root.mainloop()