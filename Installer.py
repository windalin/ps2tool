"""Glorified file copier."""

# TODO: installing in C:\Program Files requires admin privileges (oops), use an empty default path for now

import sys
sys.path.append("./ps2tool")

from CustomClasses import MyButton, MyCheckbutton, MyEntry

from distutils.dir_util import copy_tree
from os import path, rename, startfile, walk
from tkinter import Label, Tk, filedialog, messagebox

DEFAULT_PATH = ""

def get_size(start_path=".") -> int:
    """Taken from https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python.  Size in bytes."""
    total_size = 0
    for dirpath, dirnames, filenames in walk(start_path):
        for f in filenames:
            fp = path.join(dirpath, f)
            # skip if it is symbolic link
            if not path.islink(fp):
                total_size += path.getsize(fp)

    return total_size

def browse_installation_path():
    path = filedialog.askdirectory()
    if path != "":
        installation_path_entry.clear()
        installation_path_entry.set_text(path + "/ps2tool")

def install():
    installation_path = installation_path_entry.get()
    valid_path = path_check(installation_path)

    if valid_path:
        copy_tree("./ps2tool", installation_path)

    w = ""
    if no_console.get_value():
        w = "w"
        rename(installation_path + "/ps2tool.py", installation_path + "/ps2tool.pyw")

    messagebox.showinfo("Installation complete", f"Installation complete.  You can create a shortcut for ps2tool.py{w} and change its icon to LaunchPad.ico from your Planetside 2 folder.")
    startfile(installation_path)
    root.destroy()

def path_check(installation_path):
    if path.isdir(installation_path) or path.isfile(installation_path):
        return False
    
    return True

if __name__ == "__main__":
    root = Tk()
    root.title("ps2tool installer")
    root.geometry("520x180")
    Label(root, text="Installation Path:").place(x=11, y=10)
    installation_path_entry = MyEntry(root, width=60)
    installation_path_entry.set_text(DEFAULT_PATH)
    installation_path_entry.place(x=13, y=35)
    MyButton(root, text="Browse...", width=13, command=browse_installation_path).place(x=400, y=30)
    no_console = MyCheckbutton(root, True)
    no_console.place(x=8, y=70)
    Label(root, text="No console (.pyw instead of .py)", borderwidth=2).place(x=30, y=71)
    disk_space_required = str(round(get_size("./ps2tool") / 1000, 2))
    Label(root, text=f"At least {disk_space_required} KB of free disk space is required.").place(x=11, y=110)
    MyButton(root, text="Install", width=13, command=install).place(x=11, y=135)
    root.mainloop()