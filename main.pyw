from ttkwidgets.autocomplete import AutocompleteEntry
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
    

FONT = ("Helvetica", 14)
root = tk.Tk()
root.title("Script Analysis")
root.geometry("855x200")
root.resizable(False, False)

style = ttk.Style()
style.configure("Treeview",
    background="silver",
    foreground="black",
    rowheight=25,
    fieldbackground="silver",
    font=FONT
)
style.configure("Treeview.Heading", font=FONT)
style.configure('my.TButton', font=('Helvetica', 12))
style.configure("Entry", font=FONT)
style.map('Treeview', background=[('selected', 'green')]
)

main_tree = ttk.Treeview(root, height=2,)

main_tree['columns'] = ("Script", "Lot Size", "Margin", "SL pts.", "TP pts.", "SL amt.", "TP amt.", "Risk %")

# Formating columns
main_tree.column("#0", width=90, minwidth = 90)
main_tree.column("Script", width=90, minwidth = 50)
main_tree.column("Lot Size", width=80, minwidth = 50)
main_tree.column("Margin", width=80, minwidth = 50)
main_tree.column("SL pts.", width=70, minwidth = 50)
main_tree.column("TP pts.", width=70, minwidth = 50)
main_tree.column("SL amt.", width=90, minwidth = 50)
main_tree.column("TP amt.", width=90, minwidth = 50)
main_tree.column("Risk %", width=90, minwidth = 50)

# formatting Headers
main_tree.heading("#0", text="Type")
main_tree.heading("Script", text="Script")
main_tree.heading("Lot Size", text="Lot Size")
main_tree.heading("Margin", text="Margin")
main_tree.heading("SL pts.", text="SL Pts.")
main_tree.heading("TP pts.", text="TP Pts.")
main_tree.heading("SL amt.", text="SL Amt.")
main_tree.heading("TP amt.", text="TP Amt.")
main_tree.heading("Risk %", text="Risk %")

main_tree.tag_configure(tagname="green", background="#4feb34")
main_tree.tag_configure(tagname="orange", background="#eb8f34")
main_tree.tag_configure(tagname="red", background="#f03329")


#summary_tree = ttk.Treeview(root)
#summary_tree['columns'] = ('tot. loss', 'tot. profit', 'tot. rr%', 'tot. margin')



script_var = tk.StringVar(root)
sl_var = tk.StringVar(root)
rr_var = tk.StringVar(root, value=read_write()[1])
risk_var = tk.StringVar(root)
price_var = tk.StringVar(root)
balance_var = tk.StringVar(root, value=read_write()[0])

options = [x[0] for x in db.get_script_options()]

script_search = AutocompleteEntry(root, textvariable=script_var, width=10, completevalues=options,font=FONT)

sl_entry = ttk.Entry(root, textvariable=sl_var, width=10, font=FONT)
rr_entry = ttk.Entry(root, textvariable=rr_var, width=10, font=FONT)
risk_entry = ttk.Entry(root, textvariable=risk_var, width=10, font=FONT)
price_entry = ttk.Entry(root, textvariable=price_var, width=10, font=FONT)
balance_entry = ttk.Entry(root, textvariable=balance_var, width=10, font=FONT)

# labels
script_txt = tk.Label(root, text="Script", font=FONT)
sl_txt = tk.Label(root, text="SL pts.", font=FONT)
rr_txt = tk.Label(root, text="RR Factor", font=FONT)
risk_txt = tk.Label(root, text="Risk %", font=FONT)
price_txt = tk.Label(root, text="Price", font=FONT)
balance_txt = tk.Label(root, text="Balance", font=FONT)

script_txt.place(x=10, y=10)
sl_txt.place(x=135, y=10)
rr_txt.place(x = 255, y = 10)
balance_txt.place(x=375, y=10)
risk_txt.place(x=495, y=10)
price_txt.place(x=615, y=10)

script_search.place(x=10, y=40)
sl_entry.place(x=135, y=40)
rr_entry.place(x = 255, y = 40)
balance_entry.place(x=375, y=40)
risk_entry.place(x=495, y=40)
price_entry.place(x=615, y=40)

main_tree.place(x=10, y=90)

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
    risk_per = float(risk_var.get())
    price = float(price_var.get())
    if read_write() != (balance, rr):
        read_write('w', (balance, rr))
    
    script_name = script_search.get()
    sl_value = float(sl_entry.get())
    
    data = db.get_row(script_name, sl_value, *read_write(), risk_per, price)
    tag_val = rr_highlight_color(float(data["Futures"][-1]))
    main_tree.delete(*main_tree.get_children())
    main_tree.insert('', index='end', text="Futures",values=data["Futures"], tag=tag_val)
    main_tree.insert('', index='end', text="Equity",values=data["Equity"])
    


insert_button = ttk.Button(root, text="Enter", command=insert_script, style="my.TButton")
insert_button.place(x =740, y=40)


root.mainloop()