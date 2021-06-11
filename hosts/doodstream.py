#!/usr/bin/python3
#Thanks to URLResolver https://github.com/tvaddonsco/script.module.urlresolver/blob/master/lib/urlresolver/plugins/doodstream.py

from time import time
from random import choice
from scrapers.utils import headers
from urllib.parse import quote_plus
from string import ascii_letters, digits
from re import DOTALL, search as re_match
from cloudscraper import create_scraper as cl_scrape
from hosts.exceptions.exceptions import VideoNotAvalaible

scrape = cl_scrape()
host = "https://dood.to"

class Metadata:
	def __init__(self):
		self.logo = "https://i.doodcdn.com/img/logo-s.png"
		self.icon = "https://doodstream.com/favicon.ico"

def append_headers(headers):
	headers_str = "|%s" % "&".join(
		[
			"%s=%s" % (
				key, quote_plus(headers[key])
			)
			for key in headers
		]
	)

	return headers_str

def randomize(data):
	t = ascii_letters + digits

	idk = "".join(
		[
			choice(t)
			for _ in range(10)
		]
	)

	return f"{data}{idk}"

def get_video(url, referer, times = 0):
	global scrape

	resp = scrape.get(url, headers = headers)
	data = resp.text

	match = re_match(
		r'''dsplayer\.hotkeys[^']+'([^']+).+?function\s*makePlay.+?return[^?]+([^"]+)''',
		data, DOTALL
	)

	if (not match) and (times < 4):
		times += 1
		scrape = cl_scrape()
		return get_video(url, referer, times = times)

	if match:
		headers['Referer'] = url
		url_md5, token = match.groups()
		ret = scrape.get(f"{host}{url_md5}", headers = headers).text

		video_url = "{}{}{}{}".format(
			randomize(ret), token,
			int(time() * 1000), append_headers(headers)
		)

		return video_url
	else:
		raise VideoNotAvalaible(url)