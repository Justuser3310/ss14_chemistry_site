class reag__:
	def __init__(self, comps, out, category = '-'):
		# {'инапровалин': 1, 'углерод': 1}
		self.comps = comps
		# 2
		self.out = out
		# medicine
		self.category = category
	def get_all(self):
		return [self.comps, self.out, self.category]

