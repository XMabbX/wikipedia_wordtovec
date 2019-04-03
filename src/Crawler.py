import time
import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, initial_page="Wikipedia"):
        self.base_link = "https://en.wikipedia.org/wiki/"
        self.done_links = []
        self.set_of_new_links = set([initial_page])

    def get_next_page_name(self):
        return_link = ''
        while(not return_link and len(self.set_of_new_links)):
                return_link = self.set_of_new_links.pop()
                if return_link in self.done_links:
                    return_link = ''
        return return_link
        
    def generate_page_link(self, page_name):
        return self.base_link + page_name
    
    def collect_page_links(self, page_name):
        # Check if page already collected
        page_link = self.generate_page_link(page_name)
        self.done_links.append(page_link)
        html = self.make_request(page_link)
        b = BeautifulSoup(html.text, 'lxml')

        for i in b.find_all(name = 'li'):
            for link in i.find_all('a', href=True):
                link_name = link['href']
                if(link_name.startswith('/wiki/') and ':' not in link_name ):
                    if '#' in link_name:
                        link_name = link_name.split('#')[0]
                    link_name = link_name[6:]
                    self.set_of_new_links.add(link_name)
                
    def make_request(self, link):
        # Make protections
        print("Requesting ", link)
        html = requests.get(link)

        return html

    def crawl(self, maxdepth=1):
        for _ in range(maxdepth):
            print("Num of links to process: ", self.get_num_of_links_to_process())
            next_page_name = self.get_next_page_name()
            self.collect_page_links(next_page_name)
            time.sleep(1)

    def print(self):
        print("Links to process:")
        for elem in self.set_of_new_links:
            print(elem)
        print("Links processed:")
        for elem in self.done_links:
            print(elem)

    def get_num_of_links_to_process(self):
        return len(self.set_of_new_links)

    def get_num_of_collected_links(self):
        return len(self.set_of_new_links)+len(self.done_links)


craw = Crawler()
craw.crawl(10)
craw.print()
print(craw.get_num_of_collected_links())

