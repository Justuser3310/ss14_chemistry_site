class reag__:
	def __init__(self, category: str = '-', comps = {}, out: int = 0):
		# medicine
		self.category = category
		# {'инапровалин': 1, 'углерод': 1}
		self.comps = comps
		# 2
		self.out = out
	def get_all(self):
		return [self.category, self.comps, self.out]

