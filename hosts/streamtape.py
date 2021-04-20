#!/usr/bin/python

from requests import get, head
#from bs4 import BeautifulSoup
from scrapers.utils import headers
from hosts.exceptions.exceptions import VideoNotAvalaible

class Metadata:
	def __init__(self):
		self.logo = "https://streamtape.com/images/Logo@2x.png"
		self.icon = "https://streamtape.com/favicon.ico"

def get_mp4(url):
	headerss = head(url)
	mp4 = headerss.headers['Location']
	return mp4

def get_video(url, referer):
	referer = ""
	headers['Referer'] = referer
	body = get(url, headers = headers).text

	"""
	parsing = BeautifulSoup(body, "html.parser")

	try:
		video_link = (
			parsing
			.find("div", id = "videolink")
			.get_text()
		)
	except AttributeError:
		raise VideoNotAvalaible(url)
	"""

	try:
		video_link = eval(
			body
			.split("innerHTML = ")[1]
			.split(";")[0]
		)
	except IndexError:
		raise VideoNotAvalaible(url)

	video_url = get_mp4("https:%s" % video_link)
	return video_url