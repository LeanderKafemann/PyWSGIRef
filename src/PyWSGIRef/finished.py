"""
Creates finished object to indicate if the server has been generated.
"""

from .exceptions import BooleanAlreadyTrueError

class OneWayBoolean:
	def __init__(self):
		self._value = False

	@property
	def value(self) -> bool:
		return self._value

	def set_true(self):
		"""
		Setzt den Wert auf True, wenn er False ist.
		"""
		if not self._value:
			self._value = True
		else:
			raise BooleanAlreadyTrueError()

finished = OneWayBoolean()