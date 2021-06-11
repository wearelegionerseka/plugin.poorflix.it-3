#!/usr/bin/python3

from hosts import hosts
from requests import get
from bs4 import BeautifulSoup
from hosts.exceptions.exceptions import VideoNotAvalaible

from scrapers.utils import (
	recognize_link, recognize_mirror,
	recognize_title, m_identify,
	get_domain, headers
)

host = "https://eurostreaming.vote/"
excapes = ["Back", "back", ""]
timeout = 4
is_cloudflare = False
special_char = "–"

def search_serie(serie_to_search):
	search_url = "{}?s={}".format(host, serie_to_search)

	body = get(
		search_url,
		headers = headers,
		timeout = timeout
	).text

	parsing = BeautifulSoup(body, "html.parser")

	json = {
		"results": []
	}

	how = json['results']

	for a in parsing.find_all("div", class_ = "container-index-post col-xs-6 col-sm-4 col-md-2-5 col-lg-2-5"):
		image = a.find("img").get("src")
		link = a.find("a").get("href")

		title = recognize_title(
			a
			.find("h2")
			.get_text()
		)

		data = {
			"title": title,
			"link": link,
			"image": image
		}

		how.append(data)

	return json

def seasons(serie_to_see):
	domain = get_domain(serie_to_see)
	body = get(serie_to_see, headers = headers).text
	parsing = BeautifulSoup(body, "html.parser")
	titles = parsing.find_all("div", class_ = "accordion-item")

	json = {
		"results": []
	}

	datas = json['results']

	for title in titles:
		season = title.find("div", id = "season")
		title_season = ""

		for a in season.find_all("span"):
			title_season += f"{a.get_text()} "

		title_season = title_season[:-1]

		info = {
			"title": title_season,
			"episodes": []
		}

		how = info['episodes']
		list_episodes_season = title.find_all("div", class_ = "episode-wrap")

		for b in list_episodes_season:
			episode = ""

			episode += (
				b
				.find("li", class_ = "season-no")
				.get_text()
			)

			episode += " %s" % (
				b
				.find("li", class_ = "other_link")
				.find("a")
				.get_text()
			)

			infos = {
				"episode": episode,
				"mirrors": []
			}

			how1 = infos['mirrors']

			for c in b.find_all("tr", class_ = "movkb"):
				tds = c.find_all("td")
				some = tds[0].find("a")

				mirror = recognize_mirror(
					some.get_text()
				)

				link_mirror = some.get("href")

				if not link_mirror:
					link_mirror = None
				else:
					link_mirror = recognize_link(link_mirror)

				try:
					hosts[mirror]

					data = {
						"mirror": mirror,
						"quality": tds[1].get_text(),
						"link": link_mirror,
						"domain": domain
					}

					how1.append(data)
				except KeyError:
					continue

			how.append(infos)

		datas.append(info)

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
			ans = input("Type the serie title which you would search: ")
			result = search_serie(ans)['results']

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

				ans = input("What serie do you want to see?: ")

				if ans in excapes:
					break
					
				index = int(ans) - 1
				serie_to_see = result[index]['link']
				seasonss = seasons(serie_to_see)['results']

				while True:
					for a in range(
						len(seasonss)
					):
						print(
							"%d): %s" % 
							(
								a + 1,
								seasonss[a]['title']
							)
						)

					ans = input("Which season do you want to see?: ")

					if ans in excapes:
						break

					index = int(ans) - 1
					episodes = seasonss[index]['episodes']

					while True:
						for a in range(
							len(episodes)
						):
							print(
								"%d): %s" % 
								(
									a + 1,
									episodes[a]['episode']
								)
							)

						ans = input("Which episode do you want to see?: ")

						if ans in excapes:
							break

						index = int(ans) - 1
						mirrors = episodes[index]['mirrors']

						while True:
							for a in range(
								len(mirrors)
							):
								print(
									"%s): %s (%s)"
									% (
										a + 1,
										mirrors[a]['mirror'],
										mirrors[a]['quality']
									)
								)

							ans = input("What service do you want to see?: ")

							if ans in excapes:
								break

							index = int(ans) - 1

							try:
								video = identify(mirrors[index])
							except VideoNotAvalaible as a:
								print(a)
								continue

							print(video)
		except KeyboardInterrupt:
			break

if __name__ == "__main__":
	menu()