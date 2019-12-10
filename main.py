import threading
from queue import Queue
import multiprocessing 
from spider import Spider
from domain import *
from pyCrawler import *

PROJECT_NAME = "Crawling Space Test"
HOMEPAGE = "https://kyburger.ch/"
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + "/queue.txt"
CRAWLED_FILE = PROJECT_NAME + "/crawled.txt"
print("Number of threads " + str(multiprocessing.cpu_count()))
NUMBER_OF_THREADS = multiprocessing.cpu_count()
queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

# Create worker threads (will die when main exits)


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# do the next job in the queue


def work():
    while True:
        url = queue.get()
        Spider.crawl_page(threading.current_thread.__name__, url)
        queue.task_done()


# each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


# Check if there are items to be crawled
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print("{} links in the queue.".format(len(queued_links)))
        create_jobs()


create_workers()
crawl()
