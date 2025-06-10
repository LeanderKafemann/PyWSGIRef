from .exceptions import ServerAlreadyGeneratedError
from .pyhtml import PyHTML
from .finished import OneWayBoolean

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