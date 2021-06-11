#!/usr/bin/python3

from requests import get, post
from scrapers.utils import headers
from scrapers.js_hunt import unpack, decode
from re import DOTALL, findall, search as re_match
from hosts.exceptions.exceptions import VideoNotAvalaible

host = "https://userload.co"
blurl = f"{host}/api/assets/userload/js/videojs.js"
api_url = "https://userload.co/api/request/"

class Metadata:
	def __init__(self):
		self.logo = None
		self.icon = None

def get_video(url, referer):
	body = get(url, headers = headers).text

	try:
		packed = re_match(r"(eval\(function\(p,a,c,k,e,d\).*?)\s*<", body, DOTALL).group(1)
	except AttributeError:
		raise VideoNotAvalaible(url)

	unpacked = unpack(packed)
	found = findall('var (\w+)="([^"]+)', unpacked, DOTALL)

	for m in found:
		globals()[m[0]] = m[1]

	videojs = get(blurl, headers = headers).text
	decoded = decode(videojs)

	post_var = eval(
		re_match("t.send\(([^\)]+)", decoded, DOTALL).group(1)
	)

	post_var = (
		post_var
		.replace("=", " ")
		.replace("&", " ")
		.split(" ")
	)

	data = {
		post_var[0]: post_var[1],
		post_var[2]: post_var[3]
	}

	video_url = post(api_url, data, headers = headers).text
	return video_url[:-1]