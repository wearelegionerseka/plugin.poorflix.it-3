#!/usr/bin/python3

from requests import get
from bs4 import BeautifulSoup
from scrapers.utils import headers
from re import DOTALL, search as re_match
from hosts.exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = "https://vidoza.net/images-newtheme/logo_60.png"
		self.icon = "https://vidoza.net/favicon.ico?v=2"

def get_video(url, referer):
	headers['Referer'] = referer
	body = get(url, headers = headers).text
	print(body)
	"""parsing = BeautifulSoup(body, "html.parser")

	try:
		video_url = (
			parsing
			.find("source")
			.get("src")
		)
	except AttributeError:
		raise VideoNotAvalaible(url)

	return video_url"""

print(get_video("https://streamon.to/d/bt6asskue8mw", ""))