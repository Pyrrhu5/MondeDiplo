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

		# NikoNiko config

		self.url = self._get_env(
			"url",
			safe=False,
			default="https://www.monde-diplomatique.fr"
		)
		self.username = self._get_env("username", safe=False)
		self.password = self._get_env("password", safe=True)


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
