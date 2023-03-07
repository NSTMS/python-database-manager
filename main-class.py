import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector


class Database():
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("python database manager")
        self.app_width = 800
        self.app_height = 600
        self.screen_width = self.app.winfo_screenwidth()
        self.screen_height = self.app.winfo_screenheight()
        self.x = (self.screen_width / 2) - (self.app_width / 2)
        self.y = (self.screen_height / 2) - (self.app_height / 2)
        self.app.geometry(f'{self.app_width}x{self.app_height}+{int(self.x)}+{int(self.y)}')
        self.conn = mysql.connector.connect(host='localhost',user='root',passwd='',database='')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SHOW DATABASES")

        self.dataBasesNames = []
        for databases in self.cursor:
            self.dataBasesNames.append(databases)
        self.defaultValueForDbCombobox = tk.StringVar(value=self.dataBasesNames[0])
        self.dbCombobox = ttk.Combobox(self.app, values=self.dataBasesNames, textvariable=self.defaultValueForDbCombobox)
        self.dbCombobox.grid(column=0,row=0,padx=20,pady=20)

        self.dbTablesNames = []
        self.defaultValueForTablesCombobox = tk.StringVar(value="")
        self.tablesCombobox = ttk.Combobox(self.app, values=self.dbTablesNames,textvariable=self.defaultValueForTablesCombobox)
        self.tablesCombobox.grid(row=0, column=1, padx=20, pady=20)
        self.treeView = ttk.Treeview(self.app)
        self.treeView.grid(row=1, column=0)

        self.showSelectedTables(self.dbCombobox.get())
        self.dbCombobox.bind("<<ComboboxSelected>>", lambda disa: self.showSelectedTables(self.dbCombobox.get()))
        self.tablesCombobox.bind("<<ComboboxSelected>>", lambda to: self.showSelectedTables(self.dbCombobox.get()))
        self.treeView.bind('<<TreeviewSelect>>', lambda jebac: self.handleTreeViewSelectRecord())
        self.app.mainloop()
    def showSelectedTables(self, databaseName):
        print(databaseName)
        self.cursor.execute(f"USE {databaseName}")
        self.cursor.execute("SHOW TABLES")
        self.dbTablesNames = []
        for table in self.cursor:
            self.dbTablesNames.append(table[0])
        self.dbTablesNames = self.dbTablesNames
        print(self.dbTablesNames)
        if len(self.dbTablesNames) > 0:
            self.defaultValueForTablesCombobox.set(self.dbTablesNames[0])
            self.tablesCombobox['values'] = self.dbTablesNames
        else:
            self.defaultValueForTablesCombobox.set("Nie ma tutaj kurwa tutaj ten tego")
            self.tablesCombobox['values'] = self.dbTablesNames

    def handleTreeViewSelectRecord(self):
        if self.dbCombobox and self.tablesCombobox:
            window = tk.Toplevel(self.app)
            window.title(f"{self.dbCombobox.get()} {self.tablesCombobox.get()}")
            window.mainloop()
    def handleDatabaseComboboxSelect(self):
        self.defaultValueForDbCombobox = ""
        self.showSelectedTables(self, self.dbCombobox.get())

if __name__ == "__main__":
    base = Database()
