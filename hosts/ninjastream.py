#!/usr/bin/python3

from requests import post
from scrapers.utils import headers
from hosts.exceptions.exceptions import VideoNotAvalaible

api_url = "https://ninjastream.to/api/video/get"

class Metadata:
	def __init__(self):
		self.logo = None
		self.icon = None

def get_video(url, referer):
	video_id = url.split("/")[-1]
	headers['Referer'] = url
	headers['X-Requested-With'] = "XMLHttpRequest"

	data = {
		"id": video_id
	}

	json = post(
		api_url, data,
		headers = headers
	).json()

	if json['status'] == "success":
		video_url = json['result']['playlist']
		return video_url
	else:
		raise VideoNotAvalaible(url)