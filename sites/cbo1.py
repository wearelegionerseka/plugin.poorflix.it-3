#!/usr/bin/python3

from hosts import hosts
from bs4 import BeautifulSoup
from requests import post, get
from hosts.exceptions.exceptions import VideoNotAvalaible

from scrapers.utils import (
	recognize_link, recognize_mirror,
	m_identify, get_domain, headers
)

host = "https://cbo1.watch/"
excapes = ["Back", "back", ""]
timeout = 4
is_cloudflare = False

def search_film(film_to_search):
	search_url = f"{host}engine/ajax/search.php"

	search_data = {
		"query": film_to_search,
		"user_hash": "2e4a7dacdce1f7ecac038c03fbab39c42fb4bd6f"
	}

	body = post(
		search_url,
		search_data,
		headers = headers,
		timeout = timeout
	).text

	parsing = BeautifulSoup(body, "html.parser")

	json = {
		"results": []
	}

	how = json['results']

	for a in parsing.find_all("a")[:-1]:
		image = None
		link = a.get("href")
		title = a.find("span").get_text()

		data = {
			"title": title,
			"link": link,
			"image": image
		}

		how.append(data)

	return json

def search_mirrors(film_to_see):
	domain = get_domain(film_to_see)
	body = get(film_to_see, headers = headers).text
	parsing = BeautifulSoup(body, "html.parser")
	parsing = parsing.find("ul", class_ = "tabs")
	array = parsing.find_all("li")
	del array[0]

	json = {
		"results": []
	}

	datas = json['results']

	for a in array:
		link_mirror = recognize_link(
			a
			.find("a")
			.get("data-link")
		)

		mirror = recognize_mirror(
			a
			.get_text()
			.lower()
		)

		quality = "720p"

		try:
			hosts[mirror]

			data = {
				"mirror": mirror,
				"quality": quality,
				"link": link_mirror,
				"domain": domain
			}

			datas.append(data)
		except KeyError:
			pass

	return json

def identify(info):
	link = info['link']
	mirror = info['mirror']
	domain = info['domain']
	link = m_identify(link)
	return hosts[mirror].get_video(link, domain)

def menu():
	while True:
		try:
			ans = input("Type the film title which you would search: ")
			result = search_film(ans)['results']

			while True:
				for a in range(
					len(result)
				):
					print(
						"%d): %s" % 
						(
							a + 1,
							result[a]['title']
						)
					)

				ans = input("What film do you want to see?: ")

				if ans in excapes:
					break

				index = int(ans) - 1
				film_to_see = result[index]['link']
				datas = search_mirrors(film_to_see)['results']

				while True:
					for a in range(
						len(datas)
					):
						print(
							"%s): %s (%s)"
							% (
								a + 1,
								datas[a]['mirror'],
								datas[a]['quality']
							)
						)

					ans = input("What film do you want to see?: ")

					if ans in excapes:
						break

					index = int(ans) - 1

					try:
						video = identify(datas[index])
					except VideoNotAvalaible as a:
						print(a)
						continue

					print(video)
		except KeyboardInterrupt:
			break

if __name__ == "__main__":
	menu()