class XBee:
	def __init__(self):
		self._callback_method = None

	def write(self, inp):
		print(inp)

	def receive(self):
		return "pass"

	def set_callback(self, callback_method):
		self._callback_method = callback_method
