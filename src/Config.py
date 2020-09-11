#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from getpass import getpass

try:
	import dotenv
except ModuleNotFoundError:
	print(
"""Missing dependencies. Run:
pip install -r requirements.txt"""
	)
	exit(1)


class Config():
	def __init__(self, saveDir):

		self.file = os.path.join(saveDir, ".env")
		dotenv.load_dotenv(self.file)

		# Le Monde Diplo config
		self.diploUrl = self._get_env(
			"urlDiplo",
			safe=False,
			default="https://www.monde-diplomatique.fr"
		)
		self.diploUsername = self._get_env("usernameDiplo", safe=False)
		self.diploPassword = self._get_env("passwordDiplo", safe=True)


		# Calibre config
		self.calibreUrl = self._get_env(
			"urlCalibre",
			safe=False,
			default="http://127.0.0.1:8080"
		)
		self.calibreUsername = self._get_env("usernameCalibre", safe=False)
		self.calibrePassword = self._get_env("passwordCalibre", safe=True)

	def _get_env(self, name, safe=False, default=None):
		if name in os.environ:
			return os.environ.get(name)
		else:
			return self._set_env(name, safe, default)

	def _set_env(self, name, safe=False, default=None):
		msg = f"Input value for {name}\n"
		if default: msg += f"Hit enter for default: {default}\n"
		if safe: msg += f"Will be saved in plain-text\n"

		if not safe:
			val = input(msg)
		else:
			val = getpass(msg)
		if default and not val: val = default

		with open(self.file, "a") as f:
			f.write(f"{name}={val}\n")
		os.environ[name] = str(val)

		return val
