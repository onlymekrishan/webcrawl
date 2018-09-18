import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
from bs4 import BeautifulSoup
import time
import re
import urllib.request


PROJECT_NAME = 'Amazon Crawler'
STRING_VALUE = 'Virtue signalling is society\'s version of Proof of Stake'
# Split the String
searchwords = STRING_VALUE.split()
HOMEPAGE = 'https://www.google.in/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()

Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

# Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()


# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items in the queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        create_jobs()


create_workers()
crawl()


def wordsearch(searchwords,searchurl):

	# Search String in URL
	with urllib.request.urlopen(searchurl) as url:
		s = url.read().decode('utf-8', 'ignore')

	for searchword in searchwords:
		regex = r"" + format(searchword)
		match = re.search(regex, s)
		print(searchword)
			# If-statement after search() tests if it succeeded
		if match:
			print('found'), match.group()
		else:
			print('did not find')
			
			
#Function to Traverse URLs

wordsearch(searchwords, HOMEPAGE)

	
	


