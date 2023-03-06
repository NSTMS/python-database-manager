import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector


class DatabaseAdmin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("database_my_admin")
        self.app_width = 800
        self.app_height = 600
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x = (self.screen_width / 2) - (self.app_width / 2)
        self.y = (self.screen_height / 2) - (self.app_height / 2)
        self.geometry(f'{self.app_width}x{self.app_height}+{int(self.x)}+{int(self.y)}')

        self.conn = None
        self.cursor = None
        self.db_list = []
        self.table_list = []
        self.headings = []
        self.current_table = ""
        self.current_db = ""

        self.create_widgets()
        self.connect_to_mysql()

        self.mainloop()

    def create_widgets(self):
        self.combo_box_db = ttk.Combobox(self, values=self.db_list)
        self.combo_box_db.pack()
        self.combo_box_db.bind("<<ComboboxSelected>>", self.show_tables)

        self.add_db_btn = ttk.Button(self, text="Add database", command=self.add_database)
        self.add_db_btn.pack()

        self.database_entry = ttk.Entry(self)
        self.database_entry.pack()

        self.combo_box_tables = ttk.Combobox(self, values=self.table_list)
        self.combo_box_tables.pack()

        self.add_table_btn = ttk.Button(self, text="Add table", command=self.add_table)
        self.add_table_btn.pack()

        self.delete_table_btn = ttk.Button(self, text="Delete table", command=self.delete_table)
        self.delete_table_btn.pack()

        self.tree = ttk.Treeview(self)
        self.tree.pack(padx=20, pady=20)

    def connect_to_mysql(self):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database=''
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute('SHOW DATABASES')
            self.db_list = [db[0] for db in self.cursor]
            self.combo_box_db["values"] = self.db_list
            self.current_db = self.db_list[0] if self.db_list else ""
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Failed to connect to the MySQL server: {error}")

    def add_database(self):
        database_name = self.database_entry.get().strip()
        if database_name:
            try:
                self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
                self.conn.commit()
                self.db_list.append(database_name)
                self.combo_box_db["values"] = self.db_list
                self.current_db = database_name
                self.database_entry.delete(0, tk.END)
            except mysql.connector.Error as error:
                messagebox.showerror("Error", f"Failed to add database: {error}")
        else:
            messagebox.showwarning("Warning", "Database name cannot be empty")
