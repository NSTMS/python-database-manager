from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry("400x300")

tree = ttk.Treeview(root)
tree.pack(fill=BOTH, expand=1)

tree.column("#0", width=0, stretch=NO)
tree.column("Button", width=100, anchor=CENTER)
tree.heading("#0", text="")
tree.heading("Button", text="Button")
for i in range(10):
    tree.insert("", "end", text=f"Item {i}", values=[f"Button {i}"])

button = Button(tree, text="Click me")
tree.insert(tree.get_children()[i], 1, text="", image="", values=[button])
button.pack()
root.mainloop()