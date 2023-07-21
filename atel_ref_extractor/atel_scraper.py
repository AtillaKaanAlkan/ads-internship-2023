import requests
from bs4 import BeautifulSoup
import time
import sys
import argparse
import pprint

parser = argparse.ArgumentParser(description = 'This script is for extracting ATels and obtaining all information related to it (publication date, authors, subjects and references to other reports)')
parser.add_argument('--atel_id', required = True, type = str)
args = parser.parse_args()
atel_id = args.atel_id

class AtelScraper:

    def __init__(self, atel_id):

        self.atel_url = 'https://www.astronomerstelegram.org/'
        self.old_gcn_url = 'http://gcn.gsfc.nasa.gov/gcn/gcn3/'
        self.new_gcn_url = 'https://gcn.nasa.gov/circulars/'

        self.links_of_interest = ['https://www.astronomerstelegram.org/?read=',  ## link to an ATel telegram
                                  'http://www.cbat.eps.harvard.edu/iau/cbet/',   ## link to an ET telegram (from CBET)
                                  'http://gcn.gsfc.nasa.gov/gcn/gcn3/']          ## link to a GCN Circular


        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
                }

        self.waiting_time = 20 #seconds
        self.atel_id = atel_id

    def first_occurence(self, l):
        idx = 0
        for k in range(len(l)):
            if l[k].text == ' Tweet ':
                idx = k
                break
        return idx

    def request_html_code(self):

        try:
            page = requests.get(url = f'{self.atel_url}/?read={self.atel_id}', headers = self.headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            time.sleep(self.waiting_time)

        except requests.exceptions.RequestException:
            print('HTTP request failed!')
            sys.exit(0)
        
        return soup
    
    def extract_fulltext(self, html_code):

        telegram_div = html_code.find('div', {'id': 'telegram'})
        fulltext = telegram_div.get_text(strip = True).split('Tweet')[1]

        return fulltext

    def extract_related_references(self, html_code):

        related_section = html_code.find_all('div', {'id': 'related'})
        
        if related_section != []: # if there is at least one related references
            links = related_section[0].find_all('a', href = lambda href: href and href.startswith("https://www.astronomerstelegram.org/?read=") and not href == 'https://www.astronomerstelegram.org/?read=')
            related_references = []
            for link in links:
                related_references.append(link['href'])
        
            return related_references
        
        else: # if there is no related references
            return []
    
    def extract_references_from_fulltext(self, html_code):

        telegram_div = html_code.find('div', {'id': 'telegram'})
        idx = self.first_occurence(telegram_div.find_all('p'))
        fulltext = telegram_div.find_all('p')[idx + 1:]
        
        fulltext_references = []
        
        for e in fulltext:
            for links_of_interest in self.links_of_interest:
                if e.find_all('a', href=lambda href: href and href.startswith(links_of_interest) and not href == links_of_interest):
                    found_links = e.find_all('a', href=lambda href: href and href.startswith(links_of_interest) and not href == links_of_interest)
                    for link in found_links:
                        if link['href'] not in fulltext_references:
                            if links_of_interest == self.old_gcn_url:
                                fulltext_references.append(self.new_gcn_url + link['href'].split(self.old_gcn_url)[1].split('.gcn3')[0])
                            else:
                                fulltext_references.append(link['href'])
        
        return fulltext_references
     
    def extract_metadata_from_atel(self):

        soup = self.request_html_code()

        metadata = {}
        
        metadata['atel_id'] = self.atel_id
        metadata['title'] = soup.find('title').text.strip()
        metadata['publication_date'] = soup.find('div', {"id": 'time'}).text.strip()
        metadata['subjects'] = soup.find('p', {"class": 'subjects'}).text.split('Subjects:')[1].strip()
        author_tags = soup.find_all('a', href=lambda href: href and "mailto" in href)
        authors = [tag.text for tag in author_tags]
        metadata['authors'] = authors
        metadata['fulltext'] = self.extract_fulltext(soup)
        metadata['related_references_links'] = self.extract_related_references(soup)
        metadata['fulltext_references_links'] = self.extract_references_from_fulltext(soup)

        return metadata
    
atelScraper = AtelScraper(atel_id = atel_id)
metadata = atelScraper.extract_metadata_from_atel()

pprint.PrettyPrinter(indent = 4).pprint(metadata)














    

