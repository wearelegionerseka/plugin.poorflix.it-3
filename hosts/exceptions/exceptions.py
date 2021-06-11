#!/usr/bin/python

class VideoNotAvalaible(Exception):
	def __init__(self, message):
		super().__init__("The video %s isn't avalaible :(" % message)