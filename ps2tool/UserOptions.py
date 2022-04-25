"""Glorified INI reader and writer"""

# TODO: may need to add rever()

from configparser import ConfigParser

class UserOptions(ConfigParser):
	def __init__(self, ini_path):
		super().__init__()
		self.ini_path = ini_path
		self.read(ini_path)

	# Properties
	#region
	@property
	def TintModeReticuleStyle(self) -> bool:
		if not self.has_option("UI", "tintmodereticulestyle") or self.get("UI", "tintmodereticulestyle") == "0":
			return False
		elif self.get("UI", "tintmodereticulestyle") == "1":
			return True
	@TintModeReticuleStyle.setter
	def TintModeReticuleStyle(self, value):
		self.set("UI", "tintmodereticulestyle", value)

	@property
	def TintModeReticuleColor(self) -> str:
		return None if not self.has_option("UI", "tintmodereticulecolor") else self.get("UI", "tintmodereticulecolor")
	@TintModeReticuleColor.setter
	def TintModeReticuleColor(self, value):
		self.set("UI", "tintmodereticulecolor", value)
	#endregion

	# Methods
	#region
	def commit_changes(self):
		with open(self.ini_path, "w") as f:
			self.write(f)
	#endregion