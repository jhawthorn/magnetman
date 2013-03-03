
import weakref

class Controller(object):
	def __init__(self):
		#self.cache = weakref.WeakValueDictionary()
		self.cache = dict()
		#self.loader = loader
	
	def __getitem__(self, name):
		try:
			return self.cache[name]
		except KeyError:
			res = self.loader(name)
			self.cache[name] = res
			return res
	
	def clear(self):
		for each in self.cache:
			del self.cache[each]
