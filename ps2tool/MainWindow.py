"""Main window UI and actions associated with its widgets."""

# TODO: currently useroptions (default) and useroptions with the full path are treated as different items instead of the same item

try:
	import pygetwindow
	import pyautogui
	HAS_ADDITIONAL_PACKAGES = True
except:
	HAS_ADDITIONAL_PACKAGES = False

from CustomClasses import MyButton, MyCheckbutton, MyCombobox, MyEntry
from UserOptions import UserOptions

from os import startfile, system
from shutil import copyfile
from time import sleep
from tkinter import Canvas, Label, PhotoImage, Tk, colorchooser, filedialog, messagebox
from tkinter.constants import *

class MainWindow:
	def __init__(self, root, settings):
		# initial setup
		#region
		self.settings = settings
		theme = settings.Theme
		self.useroptions = UserOptions(f"{settings.PS2Path}/UserOptions.ini") if settings.MostRecentINI == "UserOptions.ini" else UserOptions(settings.MostRecentINI)
		root.title("ps2tool")
		root.geometry(f"1100x300+{self.settings.MostRecentPosition}")
		self.root = root
		self.text_fg = "black" if theme=="ns" else "white"
		self.bg = "#6d1add" if theme=="vs" else "#005aaa" if theme=="nc" else "#c83939" if theme=="tr" else "#d6d6d6"
		self.bg_img = PhotoImage(file=f"./Assets/{theme}_background.png")
		self.button_img = PhotoImage(file=f"./Assets/{theme}_button.png")
		self.icon_img = PhotoImage(file=f"./Assets/{theme}_icon.png")
		self.root.wm_iconphoto(False, self.icon_img)
		self.canvas = Canvas(self.root, width=1100, height=300, bg="black")
		self.canvas.pack(expand=YES, fill=BOTH)
		self.canvas.create_image(0, 0, image=self.bg_img, anchor=NW)
		#endregion
		
		# left side
		#region
		self.canvas.create_text(11, 10, text="Choose .ttf font file", fill=self.text_fg, anchor=NW)
		self.canvas.create_text(11, 40, text="Choose .ini file", fill=self.text_fg, anchor=NW)
		self.canvas.create_text(11, 70, text="Reticule colour", fill=self.text_fg, anchor=NW)
		self.canvas.create_text(11, 100, text="Start Recursion", fill=self.text_fg, anchor=NW)
		self.font_combobox = MyCombobox(self.canvas, settings.FontsList, default_value=settings.MostRecentFont, action_on_select=self.font_selected)
		self.ini_combobox = MyCombobox(self.canvas, settings.INIList, default_value=settings.MostRecentINI, action_on_select=self.ini_selected)
		self.font_combobox.place(x=160, y=6)
		self.ini_combobox.place(x=160, y=36)
		self.start_recursion = MyCheckbutton(self.canvas, self.settings.StartRecursion, bg=self.bg, command=self.recursion_check)
		self.start_recursion.place(x=155, y=96)
		MyButton(self.canvas, text="Add .ttf font", image=self.button_img, command=lambda: self.font_combobox.add_option(".ttf")).configure_defaults(self.bg).place(x=550, y=4)
		MyButton(self.canvas, text="Add .ini file", image=self.button_img, command=lambda: self.ini_combobox.add_option(".ini")).configure_defaults(self.bg).place(x=550, y=34)
		MyButton(self.canvas, text="Apply changes", image=self.button_img, command=self.apply_changes).configure_defaults(self.bg).place(x=8, y=125)
		MyButton(self.canvas, text="Choose reticule colour", image=self.button_img, command=self.choose_reticule_colour).configure_defaults(self.bg).place(x=550, y=64)

		if self.useroptions.TintModeReticuleStyle and self.useroptions.TintModeReticuleColor:
			self.reticule_label = Label(self.canvas, text=self.useroptions.TintModeReticuleColor, width=18, fg="white", bg=decimal_to_rgb(self.useroptions.TintModeReticuleColor), relief="groove")
		else:
			self.reticule_label = Label(self.canvas, text="disabled", width=18, fg="white", bg="black", relief="groove")
		self.reticule_label.place(x=160, y=66)
		#endregion

		# right side
		#region
		self.fetch_text = self.canvas.create_text(720, 10, text="Getting server population from honu API...", fill=self.text_fg, anchor=NW)
		self.server_combobox = MyCombobox(self.canvas, ["Connery", "Miller", "Cobalt", "Emerald", "SolTech"], default_value=settings.MostRecentWorld, width=15, action_on_select=self.update_population)
		self.server_combobox.place(x=973, y=6)
		self.canvas.create_text(720, 40, text="VS:", fill=self.text_fg, anchor=NW)
		self.canvas.create_text(720, 70, text="TR:", fill=self.text_fg, anchor=NW)
		self.canvas.create_text(720, 100, text="NC:", fill=self.text_fg, anchor=NW)
		self.canvas.create_text(720, 130, text="Wandering bots:", fill=self.text_fg, anchor=NW)
		self.vs_bar = Label(self.canvas, bg="#9656eb", width=0, borderwidth=2, relief="raised")
		self.tr_bar = Label(self.canvas, bg="#820000", width=0, borderwidth=2, relief="raised")
		self.nc_bar = Label(self.canvas, bg="#3089db", width=0, borderwidth=2, relief="raised")
		self.vs_bar.place(x=745, y=38)
		self.tr_bar.place(x=745, y=68)
		self.nc_bar.place(x=745, y=98)
		self.vs_percent = self.canvas.create_text(1010, 40, text="", fill=self.text_fg, anchor=NE)
		self.tr_percent = self.canvas.create_text(1010, 70, text="", fill=self.text_fg, anchor=NE)
		self.nc_percent = self.canvas.create_text(1010, 100, text="", fill=self.text_fg, anchor=NE)
		self.vs_pop = self.canvas.create_text(1017, 40, text="", fill=self.text_fg, anchor=NW)
		self.tr_pop = self.canvas.create_text(1017, 70, text="", fill=self.text_fg, anchor=NW)
		self.nc_pop = self.canvas.create_text(1017, 100, text="", fill=self.text_fg, anchor=NW)
		self.total_pop = self.canvas.create_text(975, 130, text="", fill=self.text_fg, anchor=NW)
		self.wandering_bots = self.canvas.create_text(810, 130, text="", fill=self.text_fg, anchor=NW)
		MyButton(self.canvas, text="Reset settings", image=self.button_img, command=self.reset_settings).configure_defaults(self.bg).place(x=717, y=155)
		MyButton(self.canvas, text="Change theme", image=self.button_img, command=self.change_theme).configure_defaults(self.bg).place(x=717, y=185)
		MyButton(self.canvas, text="I don't want to play", image=self.button_img, command=self.i_dont_want_to_play).configure_defaults(self.bg).place(x=717, y=215)
		#endregion

	# Properties
	#region
	@property
	def Worlds(self):
		return self.worlds
	@Worlds.setter
	def Worlds(self, value):
		self.worlds = value
	#endregion

	# Methods
	#region
	def change_theme(self):
		from FirstTime import ChooseThemeWindow
		self.root.destroy()
		kill_launchpad()
		settings = self.settings
		root = Tk()
		choose_theme_window = ChooseThemeWindow(root, settings, position=settings.MostRecentPosition)
		root.mainloop()
		try:
			startfile("ps2tool.pyw")
		except:
			startfile("ps2tool.py")

	def font_selected(self):
		font_path = self.font_combobox.get()
		self.settings.MostRecentFont = font_path

	def ini_selected(self, event=None):
		"""Upon selecting a different .ini file, create a new UserOptions object and update UI widgets accordingly."""
		ini_path = self.ini_combobox.get()
		self.settings.MostRecentINI = ini_path
		self.useroptions = UserOptions(ini_path)
		if not self.useroptions.TintModeReticuleStyle:
			self.reticule_label.config(text="disabled", fg="white", bg="black")
			return
		else:
			if not self.useroptions.TintModeReticuleColor:
				self.useroptions.TintModeReticuleColor = "0"
		
		self.reticule_label.configure(text=self.useroptions.TintModeReticuleColor, fg=black_or_white(self.useroptions.TintModeReticuleColor), bg=decimal_to_rgb(self.useroptions.TintModeReticuleColor))
	
	def choose_reticule_colour(self):
		"""Very messy method."""
		# TODO: this does not work properly if tintmodereticulestyle is 1 but tintmodereticulecolor does not exist
		if not self.useroptions.TintModeReticuleStyle:
			if messagebox.askquestion("tintmodereticulestyle", f"TintModeReticuleStyle is not enabled in {self.settings.MostRecentINI}, do you wish to enable it?", icon="question") == "no":
				return
			else:
				self.useroptions.TintModeReticuleStyle = "1"
				if self.useroptions.TintModeReticuleColor:
					self.reticule_label.configure(text=self.useroptions.TintModeReticuleColor, fg=black_or_white(self.useroptions.TintModeReticuleColor), bg=decimal_to_rgb(self.useroptions.TintModeReticuleColor))
		
		colour = colorchooser.askcolor(decimal_to_rgb(self.useroptions.TintModeReticuleColor))[1]
		if colour:
			self.useroptions.TintModeReticuleColor = str(rgb_to_decimal(colour))
			self.reticule_label.configure(text=self.useroptions.TintModeReticuleColor, fg=black_or_white(self.useroptions.TintModeReticuleColor), bg=decimal_to_rgb(self.useroptions.TintModeReticuleColor))

	def recursion_check(self):
		if not self.settings.RecursionPath:
			recursion_path = filedialog.askopenfilename()
			if not recursion_path.endswith("RTST.exe"):
				if recursion_path != "":
					messagebox.showerror("RTST.exe", "You need to select RTST.exe")
				self.start_recursion.set_value(False)
				return
			else:
				self.start_recursion.set_value(True)
				self.settings.RecursionPath = recursion_path

		self.settings.StartRecursion = self.start_recursion.get_value()

	def apply_changes(self):
		self.settings.FontsList = self.font_combobox.get_all()
		self.settings.INIList = self.ini_combobox.get_all()
		self.settings.MostRecentPosition = f"{self.root.winfo_x()}+{self.root.winfo_y()}"
		self.settings.commit_changes()
		self.useroptions.commit_changes()

		if self.settings.MostRecentFont != "default (Geo-Md.ttf)":
			try:
				copyfile(self.settings.MostRecentFont, self.settings.PS2Path + "/UI/Resource/Fonts/Geo-Md.ttf")
			except Exception as e:
				messagebox.showerror("Error copying font", e)

		if self.settings.MostRecentINI != "UserOptions.ini":
			try:
				copyfile(self.settings.MostRecentINI, self.settings.PS2Path + "/UserOptions.ini")
			except Exception as e:
				messagebox.showerror("Error copying .ini", e)


		if HAS_ADDITIONAL_PACKAGES:
			click_play()

		if self.settings.StartRecursion:
			startfile(self.settings.RecursionPath)

		self.root.destroy()

	def reset_settings(self):
		if messagebox.askquestion("Reset settings", "Are you sure you want to reset all settings?  This cannot be undone.", icon="question") == "no":
			return
		else:
			kill_launchpad()
			self.settings.PS2Path = ""
			self.settings.RecursionPath = ""
			self.settings.StartRecursion = False
			self.settings.FontsList = "default (Geo-Md.ttf)"
			self.settings.MostRecentFont = "default (Geo-Md.ttf)"
			self.settings.INIList = "UserOptions.ini"
			self.settings.MostRecentINI = "UserOptions.ini"
			self.settings.MostRecentWorld = "Connery"
			self.settings.Theme = ""
			self.settings.MostRecentPosition = "0+0"
			self.settings.FirstTime = True
			self.settings.commit_changes()
			restart = messagebox.askquestion("Reset and restart", "Settings have been reset.  Do you want to restart ps2tool?", icon="info")
			self.root.destroy()

			if restart == "yes":
				try:
					startfile("ps2tool.pyw")
				except:
					startfile("ps2tool.py")

	def i_dont_want_to_play(self):
		kill_launchpad()
		self.settings.revert()
		self.settings.MostRecentPosition = f"{self.root.winfo_x()}+{self.root.winfo_y()}"
		self.settings.commit_changes()
		self.root.destroy()

	def update_population(self, event=None, world_name=None):
		if world_name:
			world = self.worlds[world_name]
		else:
			world = self.worlds[self.server_combobox.get()]

		self.settings.MostRecentWorld = self.server_combobox.get()
		vs_percent = round((world.VSPop / world.TotalPopLessWanderingBots) * 100)
		tr_percent = round((world.TRPop / world.TotalPopLessWanderingBots) * 100)
		nc_percent = round((world.NCPop / world.TotalPopLessWanderingBots) * 100)
		max_percent = max(vs_percent, tr_percent, nc_percent)
		self.vs_bar.configure(width=round((vs_percent / max_percent) * 30))
		self.tr_bar.configure(width=round((tr_percent / max_percent) * 30))
		self.nc_bar.configure(width=round((nc_percent / max_percent) * 30))
		self.canvas.itemconfig(self.vs_percent, text=f"{vs_percent}%  |")
		self.canvas.itemconfig(self.tr_percent, text=f"{tr_percent}%  |")
		self.canvas.itemconfig(self.nc_percent, text=f"{nc_percent}%  |")
		self.canvas.itemconfig(self.vs_pop, text=str(world.VSPop))
		self.canvas.itemconfig(self.tr_pop, text=str(world.TRPop))
		self.canvas.itemconfig(self.nc_pop, text=str(world.NCPop))
		self.canvas.itemconfig(self.total_pop, text=f"Total  |  {world.TotalPop}")
		self.canvas.itemconfig(self.wandering_bots, text=str(world.WanderingBots))
	#endregion

# other functions
#region
def kill_launchpad():
	launchpad_kill_code = system("taskkill /f /t /im LaunchPad.exe")
	if launchpad_kill_code == 0:
		print("LaunchPad.exe killed.")
	else:
		print(f"LaunchPad.exe not killed, taskkill code: {launchpad_kill_code}")

def click_play():
	# TODO: this may not always work properly
	try:
		launchpad_window = pygetwindow.getWindowsWithTitle("Planetside 2")[0]
		launchpad_window.activate()
		play_x = launchpad_window.left + int(launchpad_window.width*0.83)
		play_y = launchpad_window.top + int(launchpad_window.height*0.85)

		while True:
			if pygetwindow.getActiveWindowTitle() == "Planetside 2":
				break
			sleep(0.07)

		pyautogui.click(play_x, play_y)
	except:
		print("Launchpad window not found")
		return

def black_or_white(decimal: str):
	"""Taken from https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color."""
	rgb = decimal_to_rgb(decimal, return_tuple=True)
	
	return "black" if (rgb[0]*0.299 + rgb[1]*0.587 + rgb[2]*0.114) > 150 else "white"

def decimal_to_rgb(decimal: str, return_tuple=False):
	"""Converts a decimal colour string to rgb, I forgot how this even works"""
	if decimal:
		binary_colour  = bin(int(decimal))[2:]
		binary_colour = (24 - len(binary_colour)) * "0" + binary_colour
		rgb_tuple = (int(binary_colour[:8], 2), int(binary_colour[8:16], 2), int(binary_colour[16:], 2))

		return rgb_tuple if return_tuple else "#%02x%02x%02x" % rgb_tuple

def rgb_to_decimal(rgb):
	return int(rgb[1:], 16) if rgb.startswith("#") else int(rgb, 16)
#endregion