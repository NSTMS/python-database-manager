from tkinter import *
from tkinter import ttk
import mysql.connector
import re
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter.simpledialog import askstring, askinteger
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

addDbBtn = Button(root, text="Add database", command=lambda: addDb())
addDbBtn.pack()
databaseEntry = Entry(root)
databaseEntry.pack()

tableList = []
if not tableList:
    default_table = StringVar(value="")
else:
    default_table = StringVar(value=tableList[0])
    currentTable = default_table

combo_box_tables = ttk.Combobox(root, textvariable=default_table)
combo_box_tables.pack()

addTableToDb = Button(root, text="Add table", command=lambda: addTable(combo_box.get()))
deleteTableFromDb = Button(root, text="Delete table", command=lambda: removeTable(combo_box.get()))
addTableToDb.pack()
deleteTableFromDb.pack()
tree = ttk.Treeview(root)
window = None
windows = []
tree.pack(padx=20)


def removeTable(baseName):
    global combo_box_tables
    table = combo_box_tables.get()
    answer = askyesno(title='confirmation',message=f'czy chcesz usunąc tabele {table}')
    if answer:
        global conn
        global cursor
        cursor.execute(f"USE {baseName}")
        cursor.execute(f"DROP TABLE {table}")
        conn.commit()
        return showSelectedDataBase(baseName)
def addTable(baseName):
    addingTableView = Toplevel(window, padx=20)
    addingTableView.title("add new Table")

    Label(addingTableView, text="Nazwa tabeli: ").grid(row=0, column=0)
    Entry(addingTableView, name="name").grid(row=0, column=1)
    Label(addingTableView, text="Ilosc kolumn: ").grid(row=1, column=0)
    Entry(addingTableView, name="quantity").grid(row=1, column=1)
    label = Label(addingTableView, text="")

    Button(addingTableView, text="add", command=lambda: validate()).grid(row=2, column=0)
    Button(addingTableView, text="close", command=lambda: closeWindow(addingTableView)).grid(row=2, column=1)

    def validate():
        if validateEntries(addingTableView.nametowidget("name").get(), addingTableView.nametowidget("quantity").get()):
            label["text"] = ""
            tablename = str(addingTableView.nametowidget("name").get())
            label.grid(row=3, column=0, columnspan=2)
            counter = int(addingTableView.nametowidget("quantity").get())
            types = ["VARCHAR(255)","TEXT","INT","FLOAT","BOOL"]
            for i in range(counter):
                Label(addingTableView, text="Nazwa: ").grid(row=3+i, column=0)
                Entry(addingTableView, name="entry_"+str(i)).grid(row=3+i, column=1)
                combobox_value = StringVar(value=types[0])
                ttk.Combobox(addingTableView,values=types ,textvariable=combobox_value,name="column_type_"+str(i)).grid(row=3+i, column=2)

            Button(addingTableView, text="submit", command=lambda: sumbitAddTable(tablename)).grid(row=counter+4, column=0)

        else:
            label["text"] = "invalid input"
            label.grid(row=3, column=0, columnspan=2)
            return

    def sumbitAddTable(name):
        counter = int(addingTableView.nametowidget("quantity").get())
        for i in range(counter):
            comboboxValue = addingTableView.nametowidget("column_type_"+str(i)).get()
            inputValue = addingTableView.nametowidget("entry_"+str(i)).get()
            valid_types = ['bigint', 'binary', 'bit', 'char', 'date', 'datetime', 'decimal', 'double', 'enum', 'float',
                           'geometry', 'geometrycollection', 'int', 'integer', 'json', 'linestring', 'longblob',
                           'longtext', 'mediumblob', 'mediumint', 'mediumtext', 'multilinestring', 'multipoint',
                           'multipolygon', 'numeric', 'point', 'polygon', 'real', 'set', 'smallint', 'text', 'time',
                           'timestamp', 'tinyblob', 'tinyint', 'tinytext', 'varbinary', 'varchar', 'year']

            if comboboxValue == "" or comboboxValue not in valid_types \
                    or inputValue == "" or inputValue == "0" or not inputValue.isalnum():
                print(inputValue, comboboxValue, inputValue.isalnum(),comboboxValue not in valid_types)
                print("invalid")
                return
            else:
                global cursor
                global conn
                print(baseName)
                cursor.execute(f"USE {baseName}")
                cursor.execute(f"CREATE TABLE IF NOT EXISTS `{name}` (Id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")
                conn.commit()
                cursor.execute(f"ALTER TABLE {name} ADD COLUMN IF NOT EXISTS {inputValue} {comboboxValue}")
                conn.commit()
                showSelectedDataBase(baseName)
        return closeWindow(addingTableView)
    addingTableView.mainloop()


def validateEntries(name, quantity):
    if quantity.isnumeric():
        for i in name:
            if not i.isalnum() or i == "":
                return False
            return True
    else:
        return False

def addDb():
    global cursor
    global combo_box_tables
    global combo_box
    global databaseEntry
    global dbList
    if databaseEntry.get() != "":
        name = re.sub('[^A-Za-z0-9]+', '', databaseEntry.get())
        cursor.execute(f"CREATE DATABASE {name};")
        databaseEntry.delete(0, END)
        conn.commit()
        dbList = []
        cursor.execute('SHOW DATABASES')
        for db in cursor:
            dbList.append(db)
        showSelectedDataBase(name)
        combo_box.set(name)
        combo_box_tables.set("")

    return


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
    global window
    if window:
        closeWindow(window)
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

    window = Toplevel(root)
    window.title(f"Details for {currentTable}")
    global windows
    windows.append(window)
    if len(tree.selection()) > 0:
        item = tree.item(tree.selection()[0])
        record = item['values']
        for i, heading in enumerate(headings):
            Label(window, text=heading).grid(row=i, column=0)
            textBox = Entry(window, name=heading.lower())
            textBox.insert(0, record[i])
            textBox.grid(row=i, column=1)
    else:
        return closeWindow(window)

    update = Button(window, text="Update",
                    command=lambda: updateSelectedElement(currentDb, currentTable, headings, record))
    update.grid(row=len(headings) + 1, column=0)

    remove = Button(window, text="Remove",
                    command=lambda: removeSelectedElement(currentDb, currentTable, headings, record))
    remove.grid(row=len(headings) + 1, column=1)

    close = Button(window, text="Close", command=lambda: closeWindow(window))
    close.grid(row=len(headings) + 2, column=0)

    window.mainloop()


def closeWindow(window):
    if window.winfo_exists() and window.winfo_name():
        window_to_close = window
        window_to_close.destroy()


def updateSelectedElement(database, table, headings, record):
    global cursor
    global window
    cursor.execute(f'USE {database}')
    set = ""
    for i, heading in enumerate(headings):
        set += " " + heading + "='" + window.nametowidget(heading.lower()).get() + "',"

    if (set.endswith(",")):
        set = set[:-1]
    cursor.execute(
        f'''UPDATE {table} SET {set} WHERE `{headings[0]}`='{record[0]}' AND `{headings[1]}`='{record[1]}' ''')
    closeWindow(window)
    showSelectedTableData(table)


def removeSelectedElement(database, table, headings, record):
    global cursor
    global window
    cursor.execute(f'USE {database}')
    if headings[0] and headings[1]:
        cursor.execute(
            f'''DELETE FROM {table} WHERE `{headings[0]}`='{record[0]}' AND `{headings[1]}`='{record[1]}' ''')
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
