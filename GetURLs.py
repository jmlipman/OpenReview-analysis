# This script will retrieve all URLs corresponding to different papers

from selenium.webdriver import Firefox # pip install selenium
import time

def get_links():
	links = []
	ta = browser.find_elements_by_xpath('//li[@class="note "]//h4//a[1]')
	# Check non-empty

	for t in ta:
		if len(t.text) > 2:
			links.append(t.get_property("href"))
	return links

URL = "https://openreview.net/group?id=ICLR.cc/2020/Conference"
filename = "urls_iclr2020.txt"

# use firefox to get page with javascript generated content
browser = Firefox()
browser.get(URL)

time.sleep(5)
urls = []
scrape = True

urls.extend(get_links())

# It will try to scrape until it cannot push the "next" button
while scrape:
	try:
		# Click next button
		nextbut = browser.find_elements_by_xpath('//li[@class="  right-arrow"]//a')
		nextbut[0].click()
		time.sleep(5)
		urls.extend(get_links())
		print(len(urls))
	except:
		scrape = False
		with open(filename, "w") as f:
			for url in urls:
				f.write(url + "\n")

print("Finished!")

