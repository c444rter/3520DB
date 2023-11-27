import mechanicalsoup as ms
import redis
import configparser
from elasticsearch import Elasticsearch, helpers

config = configparser.ConfigParser()
print(config.read('example.ini'))

es = Elasticsearch(
  cloud_id=config['ELASTIC']['cloud_id'],
  basic_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
  )

def write_to_elastic(es, url, html):
  link = url.decode('utf-8')
  es.index(index='webpages', document={ 'url' : link, 'html' : html })

def crawl(browser, r, es, url):
  browser.open(url)
  write_to_elastic(es, url, str(browser.page))  
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
    break

  crawl(browser, r, es, link)
