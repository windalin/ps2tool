"""Extend existing tkinter classes."""

from tkinter import BooleanVar, Button, Entry, Checkbutton, filedialog, messagebox, ttk, END

class MyButton(Button):
	# Methods
	#region
	def switch_state(self, condition):
		if condition:
			self["state"] = "normal"
		else:
			self["state"] = "disable"

	def configure_defaults(self, bg):
		self.configure(width=136, height=22, fg="white", bg=bg, activebackground=bg, compound="center", borderwidth=0)
		return self
	#endregion

class MyCheckbutton(Checkbutton):
	def __init__(self, parent, on_off, bg=None, command=None):
		self.my_variable = BooleanVar()
		self.my_variable.set(on_off)
		super().__init__(parent, offvalue=False, onvalue=True, variable=self.my_variable, bg=bg, activebackground=bg, command=command)

	# Methods
	#region
	def set_value(self, on_off):
		self.my_variable.set(on_off)

	def get_value(self):
		return self.my_variable.get()
	#endregion

class MyCombobox(ttk.Combobox):
	def __init__(self, parent, options_list, width=60, default_value=None, action_on_select=None):
		super().__init__(parent, values=options_list, width=width)

		if default_value:
			self.set(default_value)

		if action_on_select:
			self.action_on_select = action_on_select
			self.bind("<<ComboboxSelected>>", action_on_select)
	
	# Methods
	#region
	def add_option(self, file_extension):
		new_option = filedialog.askopenfilename()
		if new_option.endswith(file_extension):
			temp = list(self["values"])
			if new_option not in temp:
				temp.append(new_option)
			self["values"] = temp
			self.set(new_option)

			if self.action_on_select:
				self.action_on_select()

		elif new_option != "":
			messagebox.showerror("Invalid file extension", f"You need to select a {file_extension} file.")

	def get_all(self):
		return ",".join(self["values"])
	#endregion

class MyEntry(Entry):
	# Methods
	#region
	def set_text(self, text: str):
		self.clear()
		self.insert(0, text)

	def clear(self):
		self.delete(0, END)
	#endregion