class precalc__:
	def __init__(self, els):
		self.recipe = els[0]
		self.vol_in = els[1]
		self.vol_out = els[2]
	def get_all(self):
		return [self.recipe, self.vol_in, self.vol_out]
