import requests
from bs4 import BeautifulSoup
import time
import sys

class AtelScraper:

    def __init__(self, atel_id):

        self.url = 'https://www.astronomerstelegram.org/'
        
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
            page = requests.get(url = f'{self.url}/?read={self.atel_id}', headers = self.headers)
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

        related_section = html_code.find_all('div', {'id': 'related'})[0]
        related_references = related_section.find_all('a', href = lambda href: href and href.startswith("https://www.astronomerstelegram.org/?read=") and not href == 'https://www.astronomerstelegram.org/?read=')
        
        return list(related_references)
    
    def extract_references_from_fulltext(self, html_code):

        telegram_div = html_code.find('div', {'id': 'telegram'})
        idx = self.first_occurence(telegram_div.find_all('p'))
        fulltext = telegram_div.find_all('p')[idx + 1:]
        
        fulltext_references = []
        for e in fulltext:
            if e.find_all('a', href=lambda href: href and href.startswith("https://www.astronomerstelegram.org/?read=") and not href == 'https://www.astronomerstelegram.org/?read='):
                fulltext_references.append(e.find_all('a', href=lambda href: href and href.startswith("https://www.astronomerstelegram.org/?read=") and not href == 'https://www.astronomerstelegram.org/?read=')[0]['href'])

        return fulltext_references
     
    def extract_metadata_from_atel(self):

        soup = self.request_html_code()

        metadata = {}
        
        metadata['atelNumber'] = self.atel_id
        metadata['fulltext'] = self.extract_fulltext(soup)
        metadata['related_references'] = self.extract_related_references(soup)
        metadata['fulltext_references'] = self.extract_references_from_fulltext(soup)
        metadata['title'] = soup.find('title').text.strip()
        metadata['publicationDate'] = soup.find('div', {"id": 'time'}).text.strip()
        metadata['subjects'] = soup.find('p', {"class": 'subjects'}).text.split('Subjects:')[1].strip()
        author_tags = soup.find_all('a', href=lambda href: href and "mailto" in href)
        authors = [tag.text for tag in author_tags]
        metadata['authors'] = authors

        return metadata
    















    

