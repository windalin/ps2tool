"""Entry point."""

import json
import requests
import time

from MainWindow import MainWindow
from Settings import Settings
from World import World

from datetime import datetime
from os import startfile
from shutil import copyfile
from sys import exit
from threading import Thread
from tkinter import Tk, messagebox

def get_population(main_window):
	honu_url = "https://wt.honu.pw/api/population/multiple?worldID=1&worldID=10&worldID=13&worldID=17&worldID=40" # maybe use a backup fisu request in case honu doesn't work
	population = json.loads(requests.get(honu_url).text)
	fetched_time = datetime.now().strftime("%H:%M %p")

	# this order relies on honu returning results in the order of the given worldIDs
	worlds = {
		"Connery": World(population[0], name="Connery"),
		"Miller": World(population[1], name="Miller"),
		"Cobalt": World(population[2], name="Cobalt"),
		"Emerald": World(population[3], name="Emerald"),
		"SolTech": World(population[4], name="SolTech")
	}
	
	main_window.Worlds = worlds
	main_window.canvas.itemconfig(main_window.fetch_text, text=f"Server population fetched at {fetched_time}")
	main_window.update_population(world_name=settings.MostRecentWorld)

def not_top(root):
	"""Allow other windows to display over the root after 4 seconds."""
	time.sleep(4)
	root.after_idle(root.attributes, '-topmost', False)

if __name__ == "__main__":
	settings = Settings("Settings.json")
	
	if settings.FirstTime:
		import FirstTime
		FirstTime.setup(settings)
	
	root = Tk()
	
	if settings.PS2Path == "":
		root.withdraw()
		messagebox.showinfo("Path not set", "The Planetside 2 folder path is not set.  The program will now exit.")
		exit()

	if settings.Theme == None:
		exit()

	copyfile("./Assets/Geo-Md.ttf", settings.PS2Path + "/UI/Resource/Fonts/Geo-Md.ttf")
	startfile(settings.PS2Path + "/LaunchPad.exe")

	root.attributes('-topmost', True)
	main_window = MainWindow(root, settings)

	population_thread = Thread(target=get_population, args=(main_window,))
	population_thread.start()

	not_top_thread = Thread(target=not_top, args=(root,))
	not_top_thread.start()

	root.mainloop()