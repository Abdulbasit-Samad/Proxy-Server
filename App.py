import tkinter as tk
from tkinter import ttk
import subprocess
import content_filtering

blockfile = []
unblockfile = []

def submit():
    
    if port_entry.get() and int(port_entry.get()) >0 and int(port_entry.get())<=65536:
        if name_entry.get():
            blockfile.append(name_entry.get())
        if unblock_name_entry.get():
            unblockfile.append(unblock_name_entry.get())
        global port_number
        port_number = port_entry.get()
        global algorithm 
        algorithm = algorithm_var.get()
        root.destroy()

def clear_name_entry():
    if name_entry.get():
        blockfile.append(name_entry.get())
        name_entry.delete(0, tk.END)
def clear_unblock_entry():
    if unblock_name_entry.get():
        unblockfile.append(unblock_name_entry.get())
        unblock_name_entry.delete(0, tk.END)


root = tk.Tk()
root.geometry("500x300")
root.title("Proxy Server Settings")

plus_button = ttk.Button(root, text="+", command=clear_name_entry)
plus_button.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)

# Label for block website name
name_label = ttk.Label(root, text="Enter website to block:")
name_label.grid(row=0, column=0, padx=5, pady=5)

# Entry field for block website name
name_entry = ttk.Entry(root)
name_entry.grid(row=0, column=1, padx=15, pady=15)

plus_unblockbutton = ttk.Button(root, text="+", command=clear_unblock_entry)
plus_unblockbutton.grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)

# Label for unblock website name
unblock_name_label = ttk.Label(root, text="Enter website to unblock:")
unblock_name_label.grid(row=1, column=0, padx=5, pady=5)

# Entry field for unblock website name
unblock_name_entry = ttk.Entry(root)
unblock_name_entry.grid(row=1, column=1, padx=15, pady=15)

# Label for port number
port_label = ttk.Label(root, text="Enter port number:")
port_label.grid(row=2, column=0, padx=15, pady=5)

# Entry field for port number
port_entry = ttk.Entry(root)
port_entry.grid(row=2, column=1, padx=5, pady=5)

# Dropdown menu for algorithm selection
algorithm_var = tk.StringVar()
algorithm_label = ttk.Label(root, text="Choose Cache algorithm:")
algorithm_label.grid(row=3, column=0, padx=5, pady=5)
algorithm_menu = ttk.OptionMenu(root, algorithm_var, "LRU", "LRU", "LFU")
algorithm_menu.grid(row=3, column=1, padx=5, pady=5)

# Submit button
submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.grid(row=4, column=1, padx=5, pady=5)

root.mainloop()

if blockfile:
    content_filtering.block_websites(blockfile)
if unblockfile:
    content_filtering.unblock_websites(unblockfile)

if algorithm == 'LRU':
    subprocess.call(["python", "Proxy(LRU).py", port_number])
else:
    subprocess.call(["python", "Proxy(LFU).py", port_number])