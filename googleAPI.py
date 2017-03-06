from lxml import html
from urllib.parse import urlparse, parse_qs
import requests, time

headers = {
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3)'
				  'AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79'
				  'Safari/535.11',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9'
				  ',*/*;q=0.8',
	'Accept-Encoding': 'gzip,deflate,sdch',
	'Accept-Language': 'en-US,en;q=0.8',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
	}

class googleAPI:

	def __init__(self):
		self.session = requests.Session()
		self.session.headers = headers
	
	def filter_result(self, link): 
		try: 
	 
			# Valid results are absolute URLs not pointing to a Google domain 
			# like images.google.com or googleusercontent.com 
			o = urlparse(link, 'http')
			if o.netloc and 'google' not in o.netloc: 
				return link 
	 
			# Decode hidden URLs. 
			if link.startswith('/url?'): 
				link = parse_qs(o.query)['q'][0]
	 
				# Valid results are absolute URLs not pointing to a Google domain 
				# like images.google.com or googleusercontent.com 
				o = urlparse(link, 'http')
				if o.netloc and 'google' not in o.netloc: 
					return link
		# Otherwise, or on error, return None. 
		except Exception: 
			pass 
		return None

		
	def getTree(self, url):
		worked = False
		c = 0
		tree = None
		while (not worked) and (c < 5):
			try:
				times = [time.time(), time.time()]
				page = self.session.get(url, timeout=10, stream=True)
				if page.status_code != 200:
					return None
				content = b''
				for chunk in page.iter_content(chunk_size=1024):
					content += chunk
					times[1] = time.time()
					if times[1] - times[0] > 25:
						raise ValueError('StreamTimeout')
				content = content.decode('utf-8')
				tree = html.fromstring(content)
#				print("{} seconds to load {}".format((times[1]-times[0]), url))
				worked = True
			except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, ValueError):
				print("Timed out on request {}".format(url))
				return None
			except Exception as exc:
				c += 1
				raise exc
		return tree

	def getTreeTest(self):
		file = open("test.html", "rb")
		tree = html.fromstring(file.read())

		return tree
		
	def getGoogleURLs(self, q):
		hashes = set()
#		tree = self.getTree("http://google.com/search?q=" + q + "&num=100")
		tree = self.getTreeTest()
		hrefs = tree.xpath("//a/@href")
		links = []
		for s in hrefs:
			link = self.filter_result(s)
			if not link:
				continue
			h = hash(link)
			if h in hashes:
				continue
			hashes.add(h)
			links.append(link)
		return links


