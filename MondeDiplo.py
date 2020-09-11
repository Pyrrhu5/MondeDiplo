#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from src import Config

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
	CONFIG = Config(MODULE_PATH)
