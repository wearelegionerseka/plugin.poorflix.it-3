#!/usr/bin/python3

class ScrapingFailed(Exception):
	def __init__(self, message):
		super().__init__("Can not scrape %s :(" % message)