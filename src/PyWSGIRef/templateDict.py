from .exceptions import ServerAlreadyGeneratedError
from .pyhtml import PyHTML

class TemplateDict:
	def __init__(self):
		self.dictionary = {}
		self.locked = OneWayBoolean()

	def __getitem__(self, key: str) -> PyHTML:
		return self.dictionary[key]

	def __setitem__(self, key: str, value: PyHTML):
		if not isinstance(value, PyHTML):
			raise TypeError("Value must be an instance of PyHTML.")
		if not isinstance(key, str):
			raise TypeError("Key must be a string.")
		if self.locked.value:
			raise ServerAlreadyGeneratedError("Cannot modify TemplateDict after it has been locked.")
		self.dictionary[key] = value

	def __contains__(self, key: str):
		return key in self.dictionary

	def __repr__(self):
		return f"TemplateDict({self.dictionary})"

	def keys(self) -> list:
		return list(self.dictionary.keys())

	def values(self) -> list:
		return list(self.dictionary.values())

	def items(self) -> list:
		return list(self.dictionary.items())

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
			raise ValueError("Value is already True, cannot set again.")