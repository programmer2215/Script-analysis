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

def get_row(script):
    conn = sql.connect("Scripts.sqlite")
    cur = conn.cursor()
    SQL_COMMAND = f'SELECT * FROM Scripts WHERE Script = "{script.upper()}";'
    result = []
    for i in cur.execute(SQL_COMMAND):
        result.append(i)

    conn.commit()
    conn.close()
    return result

print(get_row("auBank"))

def main():
    data = load_data()
    create_table()
    reset_data(data)
    
    

if __name__ == '__main__':
    reset = input("[WARNING] do you want to Reset All Data? this action is ireversible (y/n) : ")
    if reset == 'y':
        main()
        print("ALL DATA RESET")
    
