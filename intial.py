import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Initialize GUI window
guiWindow = tk.Tk()
guiWindow.title("To-Do List")
guiWindow.geometry("400x400")
guiWindow.configure(background='#FAEBD7')

# Create database connection
the_connection = sqlite3.connect('tasks.db')
the_cursor = the_connection.cursor()

# Create tasks table if not exists
the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks(title TEXT)')

def add_task():
    task_string = task_field.get()
    if task_string == "":
        messagebox.showinfo('Error', 'Field is Empty')
    else:
        tasks.append(task_string)
        the_cursor.execute('INSERT INTO tasks VALUES(?)', (task_string,))
        list_update()
        task_field.delete(0, 'end')

def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

def delete_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            the_cursor.execute('DELETE FROM tasks WHERE title = ?', (the_value,))
    except tk.TclError:
        messagebox.showinfo('Error', 'No task selected')

def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you Sure?')
    if message_box:
        while len(tasks) != 0:
            tasks.pop()
        the_cursor.execute('DELETE FROM tasks')
        list_update()

def clear_list():
    task_listbox.delete(0, 'end')

def close():
    print(tasks)
    guiWindow.destroy()

def retrieve_database():
    while len(tasks) != 0:
        tasks.pop()
    for row in the_cursor.execute('SELECT title FROM tasks'):
        tasks.append(row[0])

tasks = []
header_frame = tk.Frame(guiWindow, bg='#FAEBD7')
function_frame = tk.Frame(guiWindow, bg='#FAEBD7')
listbox_frame = tk.Frame(guiWindow, bg='#FAEBD7')

header_frame.pack(fill='both')
function_frame.pack(side='left', expand=True, fill='both')
listbox_frame.pack(side='left', expand=True, fill='both')

header_label = ttk.Label(
    header_frame, text="To-Do List", font=("Brush Script MT", "30"), background="#FAEBD7", foreground="#8B4513")
header_label.pack(padx=20, pady=20)

task_label = ttk.Label(
    function_frame, text="Enter The Task: ", font=("Consolas", "11", "bold"), background="#FAEBD7", foreground="#000000")
task_label.place(x=30, y=40)

task_field = ttk.Entry(
    function_frame, font=("Consolas", "12"), width=18, background="#FFF8DC", foreground="#A52A2A")
task_field.place(x=30, y=80)

add_button = ttk.Button(
    function_frame, text="Add Task", width=24, command=add_task)
del_button = ttk.Button(
    function_frame, text="Delete Task", width=24, command=delete_task)
del_all_button = ttk.Button(
    function_frame, text="Delete All Tasks", width=24, command=delete_all_tasks)
exit_button = ttk.Button(
    function_frame, text="Exit", width=24, command=close)
add_button.place(x=30, y=120)
del_button.place(x=30, y=160)
del_all_button.place(x=30, y=200)
exit_button.place(x=30, y=240)

task_listbox = tk.Listbox(
    listbox_frame, width=26, height=13, selectmode='SINGLE', background="#FFFFFF", foreground="#000000", selectbackground="#CD853F", selectforeground="#FFFFFF")
task_listbox.place(x=10, y=20)

retrieve_database()
list_update()
guiWindow.mainloop()
the_connection.commit()
the_cursor.close()
