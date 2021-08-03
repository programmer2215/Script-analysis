import sqlite3 as sql
from openpyxl import load_workbook


def load_data():
    wb = load_workbook('data.xlsx')
    ws = wb.active

    column_count = ws.max_column
    row_count = ws.max_row 
    
    data_array = []

    for row in range(1, row_count + 1):
        row_array = []
        for column in range(0, column_count):
            column_id = chr(65 + column)
            cell_ref = f"{column_id}{row}"
            row_array.append(ws[cell_ref].value)
        data_array.append(tuple(row_array))
    
    return data_array

def create_table():
    conn = sql.connect("Scripts.sqlite")
    cur = conn.cursor()
    SQL_PURGE = 'DROP TABLE IF EXISTS Scripts;'
    SQL_CREATE = '''
    CREATE TABLE Scripts (
        Script TEXT,
        Lot_Size INTEGER,
        Margin INTEGER
    );
    '''
    cur.execute(SQL_PURGE)
    cur.execute(SQL_CREATE)
    conn.commit()
    conn.close()

def reset_data(data):
    conn = sql.connect("Scripts.sqlite")
    cur = conn.cursor()

    SQL_COMMAND = 'INSERT INTO Scripts VALUES (?, ?, ?);'
    cur.executemany(SQL_COMMAND, data)
    conn.commit()
    conn.close()

def get_script_options():
    conn = sql.connect("Scripts.sqlite")
    cur = conn.cursor()
    data = []
    SQL_COMMAND = "SELECT Script FROM Scripts;"
    for script in cur.execute(SQL_COMMAND):
        data.append(script)

    return data


def get_row(script, sl_pts, balance, rr):
    conn = sql.connect("Scripts.sqlite")
    cur = conn.cursor()
    SQL_COMMAND = f'SELECT * FROM Scripts WHERE Script = "{script.upper()}";'
    cur.execute(SQL_COMMAND)
    script_name, lot_sze, margin = cur.fetchall()[0]
    tp_pts = sl_pts * rr
    sl_amt = sl_pts * lot_sze
    tp_amt = tp_pts * lot_sze
    rr_percent = round((sl_amt / balance) * 100, 2)

    
    conn.commit()
    conn.close()
    return script_name, lot_sze, margin, sl_pts, tp_pts, sl_amt, tp_amt, rr_percent

def main():
    data = load_data()
    create_table()
    reset_data(data)
    
    

if __name__ == '__main__':
    reset = input("[WARNING] do you want to Reset All Data? this action is ireversible (y/n) : ")
    if reset == 'y':
        main()
        print("ALL DATA RESET")
    
