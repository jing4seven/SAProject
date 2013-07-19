'''
Customer wrapper.

'''

def singleton(cls, *args, **kwargs):
	'''
	Singleton warpper for class object.

	usage:
	@singleton
	class example(object):
		pass

	'''
	instances = {}
	def _singleton(clsa):
		if cls not in instances:
			instances[cls] = cls(*args, **kwargs)
		return instances[cls]
	return _singleton