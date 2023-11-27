import mechanicalsoup as ms
import redis

def crawl(browser, r, url):
	print("download url")
	browser.open(url)
	a_tags = browser.page.find_all("a")
	hrefs = [ a.get("href") for a in a_tags]
	wikipedia_domain = "https://en.wikipedia.org"
	links = [ wikipedia_domain + a for a in hrefs if a and a.startswith("/wiki/") ]
	r.lpush("links", *links)

browser = ms.StatefulBrowser()
r = redis.Redis()

start_url = "https://en.wikipedia.org/wiki/Redis"
r.lpush("links", start_url)

while link := r.rpop("links"):
	if "Jesus" in str(link):
		break;
	crawl(browser, r, link)
