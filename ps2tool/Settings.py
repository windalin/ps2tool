"""Glorified JSON reader and writer."""

# TODO: should use json lists instead

import json

class Settings:
	def __init__(self, filepath):
		self.filepath = filepath
		with open(self.filepath, "r") as f:
			self.original_settings = json.load(f)
			self.settings = self.original_settings.copy()

	# Properties
	#region
	@property
	def PS2Path(self) -> str:
		return self.settings["ps2_path"]
	@PS2Path.setter
	def PS2Path(self, value):
		self.settings["ps2_path"] = value

	@property
	def RecursionPath(self) -> str:
		return None if self.settings["recursion_path"] == "" else self.settings["recursion_path"]
	@RecursionPath.setter
	def RecursionPath(self, value):
		self.settings["recursion_path"] = value

	@property
	def StartRecursion(self) -> bool:
		return True if self.settings["start_recursion"] else False
	@StartRecursion.setter
	def StartRecursion(self, value):
		self.settings["start_recursion"] = value

	@property
	def FontsList(self) -> str: # should really be a list
		return self.settings["fonts_list"].split(",")
	@FontsList.setter
	def FontsList(self, value):
		self.settings["fonts_list"] = value

	@property
	def MostRecentFont(self) -> str:
		return self.settings["most_recent_font"]
	@MostRecentFont.setter
	def MostRecentFont(self, value):
		self.settings["most_recent_font"] = value

	@property
	def INIList(self) -> str: # should also be a list
		return self.settings["ini_list"].split(",")
	@INIList.setter
	def INIList(self, value):
		self.settings["ini_list"] = value

	@property
	def MostRecentINI(self) -> str:
		return self.settings["most_recent_ini"]
	@MostRecentINI.setter
	def MostRecentINI(self, value):
		self.settings["most_recent_ini"] = value

	@property
	def MostRecentWorld(self) -> str:
		return self.settings["most_recent_world"]
	@MostRecentWorld.setter
	def MostRecentWorld(self, value):
		self.settings["most_recent_world"] = value
	
	@property
	def Theme(self) -> str:
		return None if self.settings["theme"] == "" else self.settings["theme"]
	@Theme.setter
	def Theme(self, value):
		self.settings["theme"] = value

	@property
	def MostRecentPosition(self) -> str:
		return self.settings["most_recent_position"]
	@MostRecentPosition.setter
	def MostRecentPosition(self, value):
		self.settings["most_recent_position"] = value

	@property
	def FirstTime(self) -> bool:
		return True if self.settings["first_time"] else False
	@FirstTime.setter
	def FirstTime(self, value: bool):
		self.settings["first_time"] = value
	#endregion
	
	# Methods
	#region
	def commit_changes(self):
		with open(self.filepath, "w") as f:
			json.dump(self.settings, f, indent=4)

	def revert(self):
		"""Revert the settings dict to what it was upon read."""
		self.settings = self.original_settings

	def __str__(self):
		out = ""
		for i in self.settings.items():
			out = out + str(i) + "\n"
		return out.rstrip()
	#endregion