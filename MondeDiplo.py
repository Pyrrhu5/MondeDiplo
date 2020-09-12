#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from src import Config, \
				Scraper, \
				FileFormat, \
				Calibre 

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
	CONFIG = Config(MODULE_PATH)
	conn = Scraper(CONFIG.diploUrl, os.path.join(MODULE_PATH, "failed"))
	conn.connect(CONFIG.diploUsername, CONFIG.diploPassword)
	ebookPath = conn.download_latest_edition(FileFormat.epub)
	if ebookPath: print(f"Successfully downloaded ebook: {ebookPath}")
	calibre = Calibre(
		CONFIG.calibreUrl,
		CONFIG.calibreUsername,
		CONFIG.calibrePassword
	)
	calibre.add_to_library(ebookPath)
