"""Represents the current state of a server(world).  Currently only contains population info (may add more stuff in the future)."""

class World:
	worlds_dict = {
		"1": "Connery", "Connery": "1",
		"10": "Miller", "Miller": "10",
		"13": "Cobalt", "Cobalt": "13",
		"17": "Emerald", "Emerald": "17",
		"40": "SolTech", "SolTech": "40"
	}

	def __init__(self, population, name=None, id=None):
		self.population = population

		if name:
			self.name, self.id = name, self.name_id_mapper(name)
		elif id:
			self.id, self.name = id, self.name_id_mapper(id)

	# Properties
	#region
	@property
	def Name(self) -> str:
		return self.name

	@property
	def ID(self) -> str:
		return self.id

	@property
	def VSPop(self) -> int:
		return int(self.population["vs"]) + int(self.population["ns_vs"])

	@property
	def TRPop(self) -> int:
		return int(self.population["tr"]) + int(self.population["ns_tr"])

	@property
	def NCPop(self) -> int:
		return int(self.population["nc"]) + int(self.population["ns_nc"])

	@property
	def NSPop(self) -> int:
		return int(self.population["ns"])

	@property
	def WanderingBots(self) -> int:
		return int(self.population["nsOther"])

	@property
	def TotalPop(self) -> int:
		return int(self.population["total"])

	@property
	def TotalPopLessWanderingBots(self) -> int:
		"""NS pop from honu API doesn't always add up."""
		return self.VSPop + self.TRPop + self.NCPop
	#endregion

	# Methods
	#region
	@staticmethod
	def name_id_mapper(name_or_id):
		return World.worlds_dict[name_or_id]
	#endregion