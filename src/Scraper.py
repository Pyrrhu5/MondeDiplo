#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import requests
import re
from datetime import datetime


class Scraper():

	def __init__(self, url, failedDir):
		self.url = url
		self.failedDir = self._set_failed_dir(failedDir)
		self.session = None
		self.headers = {
			"User-Agent":"Mozilla/5"
		}


	def _set_failed_dir(self, failedDir):
		if not os.path.exists(failedDir):
			os.mkdir(failedDir)

		return failedDir


	def connect(self, username, password):
		print(f"Connecting to {self.url}...")
		# reset or set the session
		self.session = requests.Session()
		loginUrl = f"{self.url}/connexion"
		# grap the login page to fetch the CSRF token
		homePageResponse = self.session.get(loginUrl)
		if homePageResponse.status_code != 200:
			with open(os.path.join(self.failedDir, "failed.html"), "wb") as f:
				f.write(homePageResponse.content)
			print(f"Failed to get the home page. Status code {homePageResponse.status_code}")
			return False

		# Fetch the CSRF token
		homePageContent = homePageResponse.content
		with open("homepage.html", 'wb') as f: f.write(homePageContent)
		regexToken = re.compile(r"<input name=\\'formulaire_action_args\\' type=\\'hidden\\' value=\\'([a-zA-Z0-9_=+-]*)")
		token = regexToken.search(str(homePageContent)).group(1)
		if token == '':
		 	print("Failed to fetch the CSRF token")
		 	with open(os.path.join(self.failedDir, "failed.html"), "wb") as f:
		 		f.write(homePageResponse.content)
		 	return False

		# login
		payload = {
			"page":"connexion_sso",
			"formulaire_action":"identification_sso",
			"formulaire_action_args": token,
			"retour": "https://www.monde-diplomatique.fr/mon_compte",
			"site_distant": "https://www.monde-diplomatique.fr/",
			"email": username,
			"mot_de_passe": password,
			"valider": "Valider"
		}

		# Website uses a redirection to login
		loginUrl = "https://lecteurs.mondediplo.net/?page=connexion_sso"
		conn = self.session.post(loginUrl, data=payload, headers=self.headers)

		if conn.status_code != 200:
			print(f"Failed to connect. Status code: {conn.status_code}")
			with open(os.path.join(self.failedDir, "failed.html"), "wb") as f:
				f.write(conn.content)
			return False

		return True


	def is_connected(self):
		return self.session is not None


	def __str__(self):
		return f"Scraper object for {self.url}. Connected: {self.is_connected()}"

