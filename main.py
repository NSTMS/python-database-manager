from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter.messagebox import showinfo

root = Tk()
root.title("database_my_admin")
appWidth = 800
appHeight = 600
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
x = (screenWidth / 2) - (appWidth / 2)
y = (screenHeight / 2) - (appHeight / 2)
root.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')


conn = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database=''

)
cursor = conn.cursor()
cursor.execute('SHOW DATABASES')

dbList = []
tableList = []
headings = []
currentTable = ""
currentDb = ""
for dataBases in cursor:
    dbList.append(dataBases)

default_value = StringVar(value=dbList[0][0])
combo_box = ttk.Combobox(root, values=dbList, textvariable=default_value)
if len(dbList) != 0:
    currentDb = dbList[0][0]
    print(currentDb)
combo_box.pack()

tableList = []
if not tableList:
    default_table = StringVar(value="")
else:
    default_table = StringVar(value=tableList[0])
    currentTable = default_table

combo_box_tables = ttk.Combobox(root, textvariable=default_table)
combo_box_tables.pack()
tree = ttk.Treeview(root)
window = None
windows = []
tree.pack(padx=20)

# frame_btn = Button(root, text="Delete", command=deleteSelectedElement, width=0)
# frame_btn.pack()



def showSelectedDataBase(dbName):
    cursor.execute(f'USE {dbName}')
    cursor.execute('SHOW TABLES')

    combo_box['values'] = dbList
    tree.pack_forget()
    tableList.clear()

    for table in cursor:
        tableList.append(table[0])

    combo_box_tables['values'] = tableList

    if len(tableList) != 0:
        tree.pack()
        combo_box_tables.set(tableList[0])
        global currentTable
        currentTable = tableList[0]
        showSelectedTableData(tableList[0])

def showSelectedTableData(tableName):
    tree.delete(*tree.get_children())
    cursor.execute(f'SELECT * FROM {tableName}')
    result = cursor.fetchall()

    global headings
    headings = [i[0] for i in cursor.description]
    tree["columns"] = headings

    tree.column("#0", width=0, stretch=NO)
    for i in cursor.description:
        tree.column(i[0], width=100)
        tree.heading(i[0], text=i[0], anchor=W)
    for res in result:
        tree.insert('', END, values=res)

def item_selected(event):
    global headings
    global currentTable
    global currentDb
    global window
    global combo_box_tables
    global combo_box


    if combo_box_tables and combo_box:
        currentDb = combo_box.get()
        currentTable = combo_box_tables.get()
        print(currentDb, currentTable)

    window = Toplevel(root)
    window.title(f"Details for {currentTable}")
    global windows
    windows.append(window)
    if len(tree.selection()) > 0:
        item = tree.item(tree.selection()[0])
        record = item['values']
        for i,heading in enumerate(headings):
            Label(window, text=heading).grid(row=i, column=0)
            textBox = Entry(window)
            textBox.insert(0, record[i])
            textBox.grid(row=i, column=1)
    else:
        closeWindow(window)


    update = Button(window, text="Update", command=lambda: updateSelectedElement(currentDb, currentTable, headings, record))
    update.grid(row=len(headings)+1, column=0)

    remove = Button(window, text="Remove", command=lambda: removeSelectedElement(currentDb, currentTable,headings, record))
    remove.grid(row=len(headings)+1, column=1)

    close = Button(window, text="Close", command=lambda: closeWindow(window))
    close.grid(row=len(headings)+2, column=0)

    window.mainloop()

def closeWindow(window):
    global windows
    if window.winfo_exists() and window.winfo_name():
        window_to_close = windows.pop()
        window_to_close.destroy()
def updateSelectedElement (database,table,headings, record):
    global cursor
    cursor.execute(f'USE {database}')
    set = ""
    # cursor.execute(f'''UPDATE {table} SET {set} WHERE `{headings[0]}`='{record[0]}' AND `{headings[1]}`='{record[1]}' ''')
    showSelectedTableData(table)

def removeSelectedElement(database,table,headings, record):
    global cursor
    global window
    cursor.execute(f'USE {database}')
    print(f'''DELETE FROM {table} WHERE `{headings[0]}`='{record[0]}' AND `{headings[1]}`='{record[1]}' ''')
    cursor.execute(f'''DELETE FROM {table} WHERE `{headings[0]}`='{record[0]}' AND `{headings[1]}`='{record[1]}' ''')
    conn.commit()
    closeWindow(window)
    showSelectedTableData(table)
def onDataBaseSelect(event):
    selected_value = combo_box.get()
    default_table.set("")
    showSelectedDataBase(selected_value)

def onTablesSelect(event):
    selected_value = combo_box_tables.get()
    showSelectedTableData(selected_value)


showSelectedDataBase(dbList[0][0])
combo_box.bind("<<ComboboxSelected>>", onDataBaseSelect)
combo_box_tables.bind("<<ComboboxSelected>>", onTablesSelect)
tree.bind('<<TreeviewSelect>>', item_selected)

root.mainloop()