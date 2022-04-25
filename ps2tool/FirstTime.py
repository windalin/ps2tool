"""Sets the path to the PS2 folder and the main window's theme."""

import os

from CustomClasses import MyButton, MyEntry

from shutil import copyfile
from tkinter import Tk, Label, filedialog, messagebox

class PS2PathWindow:
	def __init__(self, root, settings):
		self.settings = settings
		root.title("Select your Planetside 2 folder")
		root.geometry("510x120")
		self.root = root
		self.ps2_path_entry = MyEntry(self.root, width=62)
		self.ps2_path_entry.grid(row=1, column=0, padx=5, sticky="W")
		self.continue_button = MyButton(self.root, text="Continue", width=13, state="disable", command=self.continue_onpress)
		self.continue_button.grid(row=2, column=0, padx=5, pady=10, sticky="W")
		Label(self.root, text="Looks like this is your first time running ps2tool.  Select your Planetside 2 folder to continue.").grid(row=0, column=0, columnspan=2, padx=5, pady=10, sticky="W")
		MyButton(self.root, text="Browse...", width=13, command=self.browse_for_path).grid(row=1, column=1, padx=5, sticky="E")

	# Methods
	#region
	def browse_for_path(self):
		path = filedialog.askdirectory()
		self.ps2_path_entry.set_text(path)
		self.continue_button.switch_state(os.path.isfile(path + "/PlanetSide2_x64.exe"))

	def continue_onpress(self):
		self.settings.PS2Path = self.ps2_path_entry.get()
		self.settings.commit_changes()
		copyfile(self.settings.PS2Path + "/UI/Resource/Fonts/Geo-Md.ttf", "./Assets/Geo-Md.ttf")
		self.root.destroy()
	#endregion

class ChooseThemeWindow:
	def __init__(self, root, settings, position=None):
		self.settings = settings
		self.root = root
		self.root.title("Choose theme")
		geometry = f"530x95+{position}" if position else "530x95"
		self.root.geometry(geometry)
		Label(self.root, text="Choose your theme:").grid(row=0, column=0, columnspan=4, padx=5, pady=10, sticky="W")
		MyButton(self.root, text="VS", width=16, bg="#8940d6", fg="white", command=lambda: self.theme_onpress("vs")).grid(row=1, column=0, padx=5)
		MyButton(self.root, text="TR", width=16, bg="#c41b1b", fg="white", command=lambda: self.theme_onpress("tr")).grid(row=1, column=1, padx=5)
		MyButton(self.root, text="NC", width=16, bg="#2a4ede", fg="white", command=lambda: self.theme_onpress("nc")).grid(row=1, column=2, padx=5)
		MyButton(self.root, text="NS", width=16, bg="#8c8c8c", fg="white", command=lambda: self.theme_onpress("ns")).grid(row=1, column=3, padx=5)

	# Methods
	#region
	def theme_onpress(self, theme):
		self.settings.Theme = theme
		self.settings.FirstTime = False # only set firsttime to false if a theme is chosen
		self.settings.commit_changes()
		self.root.destroy()
	#endregion

def setup(settings):
	root = Tk()
	ps2_path_window = PS2PathWindow(root, settings)
	root.mainloop()

	if settings.PS2Path != "":
		root = Tk()
		choose_theme_window = ChooseThemeWindow(root, settings)
		root.mainloop()