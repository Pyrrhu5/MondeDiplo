#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os

class Calibre():
	def __init__(self, url, username, password):
		self.url = url
		self.username = username
		self.password = password

	def add_to_library(self, filePath):
		print(f"Adding to Calibre\'s library {filePath}")

		cmd = f"calibredb add --with-library {self.url} --user {self.username} --password {self.password} {filePath}"

		os.system(cmd)	
