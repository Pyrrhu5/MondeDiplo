#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import requests
import re
import binascii

class Scraper():

	def __init__(self, url, failedDir):
		self.url = url
		self.failedDir = self._set_failed_dir(failedDir)
		self.session = None
		self.tempFiles = set()
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


	def _get_download_link(self, fileFormat):
		print("Getting download link...")

		url = f"{self.url}/telechargements/"
		req = self.session.get(url)
		if req.status_code != 200:
			print(f"Failed to obtain download link page: {req.status_code}")
			with open(os.path.join(self.failedDir, "failed_download.html"), "wb") as f:
				f.write(req.content)
			return None

		regex = re.compile(fr"/action/telecharger_ebook/[a-z0-9]+/diplo::[0-9]{{4}}::Le-Monde-diplomatique-[0-9]{{4}}-[0-9]{{2}}\.{fileFormat}::[a-z0-9]+")
		link = regex.search(str(req.content))

		if link:
			return f"{self.url}{link.group(0)}"
		else:
			print(f"Could not get the download link for format {fileFormat}")


	def download_latest_edition(self, fileFormat):
		print("Downloading latest edition...")
		
		headers = {
			**self.headers,
			"Host": "www.monde-diplomatique.fr",
			"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0",
			"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
			"Accept-Language": "en-GB,en;q=0.5",
			"Accept-Encoding": "gzip, deflate, br",
			"DNT": "1",
			"Connection": "keep-alive",
			"Referer": "https://www.monde-diplomatique.fr/telechargements/"
		}

		req = self.session.get(
			self._get_download_link(fileFormat),
			stream=True,
			headers=self.headers
		)
		
		if req.status_code != 200:
			print(f"Could not download the latest edition: {req.status_code}")
			return None
		else:
			filename = f"{binascii.hexlify(os.urandom(8)).decode()}.{fileFormat}"
			filepath = os.path.join("/tmp", filename)
			with open(filepath, "wb") as f:
				f.write(req.content)
			self.tempFiles.add(filepath)
			return filepath 

	def _clean_temp(self):
		print(f"Cleaning {len(self.tempFiles)} temporary file(s)...")

		while len(self.tempFiles) != 0:
			toDel = self.tempFiles.pop()
			os.remove(toDel)

	def __str__(self):
		return f"Scraper object for {self.url}. Connected: {self.is_connected()}"

	def __del__(self):
		self._clean_temp()	


class FileFormat():
	epub = "epub"
	pdf = "pdf"
	mobi = "azw3"
