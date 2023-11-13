import requests
from bs4 import BeautifulSoup
from html2text import HTML2Text
import time
import sys
import argparse
import pprint
import re
import json


parser = argparse.ArgumentParser(description = 'This script is for extracting observation reports and obtaining all information related to it (publication date, authors, subjects and references to other reports)')

parser.add_argument('--report_type', required = True, type = str)
parser.add_argument('--report_id', required = True, type = str)

args = parser.parse_args()

report_type = args.report_type
report_id = args.report_id

USE_REGULAX_EXPRESSION = True # choose to use (or not) regular expressions to find references 

class ReportScraper:

    def __init__(self):

        self.atel_url = 'https://www.astronomerstelegram.org/'
        self.old_gcn_url = 'http://gcn.gsfc.nasa.gov/gcn/gcn3/'
        self.new_gcn_url = 'https://gcn.nasa.gov/circulars/'
        
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
                }

        self._html2text = HTML2Text()
        self._html2text.ignore_emphasis = True
        self._html2text.single_line_break = False
        self._html2text.ignore_links = True
        self._html2text.body_width = 0

        self.links_of_interest = ['https://www.astronomerstelegram.org/?read=',  ## link to an ATel telegram
                                  'http://www.cbat.eps.harvard.edu/iau/cbet/',   ## link to an ET telegram (from CBET)
                                  'http://gcn.gsfc.nasa.gov/gcn/gcn3/']          ## link to a GCN Circular


        self.waiting_time = 20 #seconds
        self.report_id = report_id

    def request_html_page(self, report_type, report_id):

        if report_type == 'gcn':

            html_page = requests.get(url = f'{self.new_gcn_url}{report_id}.json', headers = self.headers)

        elif report_type == 'atel':

            html_page = requests.get(url = f'{self.atel_url}?read={self.report_id}', headers = self.headers)

        return html_page

    def extract_metadata(self, report_type, report_id):

        metadata = {}
        metadata['report_type'] = report_type
        metadata['report_id'] = int(report_id)

        if report_type == 'atel':

            html_req = self.request_html_page(report_type, report_id)
            html = BeautifulSoup(html_req.text, 'html.parser')
            html = html.find('div', id = 'telegram')

            html.find('div', id = 'tnav').decompose()
            metadata['title'] = html.find('center').extract().get_text()

            text = html.find('em').extract()
            html.find('p', align = 'CENTER').decompose()
            metadata['authors'] = text.find('strong').extract().get_text()

            metadata['publication_date'] = text.find('strong').get_text()

            text = html.find('div', id = 'subjects').extract()
            metadata['subjects'] = text.get_text().replace('Subjects:', '').strip()   
            

            html.find('a', class_= 'twitter-share-button').decompose()
            html.find('script').decompose()
            
            if html.find('p').get_text().strip() == '':
                html.find('p').decompose()
            
            metadata['fulltext'] = self._html2text.handle(repr(html)).strip()
            metadata['related_references'] = self.extract_related_references(BeautifulSoup(html_req.text, 'html.parser'))
            metadata['fulltext_hyperlinked_references'] = self.extract_hyperlinked_references_from_fulltext(BeautifulSoup(html_req.text, 'html.parser'))
            
            if USE_REGULAX_EXPRESSION:
                metadata['fulltext_references_regexp'] = self.extract_references_with_regular_expressions(metadata['fulltext'])


            return metadata

        elif report_type == 'gcn':

            html = self.request_html_page(report_type, report_id)
            
            metadata['title'] = html.json()['subject']
            metadata['authors'] = html.json()['submitter']
            metadata['publication_date'] = html.json()['createdOn']
            metadata['fulltext'] = html.json()['body']
            
            if USE_REGULAX_EXPRESSION:
                metadata['fulltext_references_regexp'] = self.extract_references_with_regular_expressions(metadata['fulltext'])

            return metadata

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

    def extract_hyperlinked_references_from_fulltext(self, html_code):

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

    def first_occurence(self, l):
        idx = 0
        for k in range(len(l)):
            if l[k].text == ' Tweet ':
                idx = k
                break
        return idx

    def extract_references_with_regular_expressions(self, text):

        regex_patterns = [
            
            # for GCN circulars
            r'GCN\s\d+',
            r'GCN\s#\d+',
            r'GCN Circ\s#\d+',
            r'GCN Circ.\s#\d+',
            
            # for ATels
            r'ATel\s#\d+',
            r'ATel#\d+',
            r'Atel#\d+',
            r'Atel\s#\d+',
            r'ATEL\s#\d+',
            r'ATEL#\d+',
            r'ATels\s#\d+',
            r"ATels\s#(\d+(?:,\s#\d+)*)",
            r"ATel\s#(\d+(?:,\s#\d+)*)",
            r"ATel\s#(\d+(?:;\s#\d+)*)",

            # for CBAT (frequently used?)
            r'CBET\s\d+'
            
        ]

        identified_expressions = []

        for pattern in regex_patterns:
            
            matches = re.finditer(pattern, text)
            
            for match in matches:
                
                expression = match.group()
                span = match.span()
                if (expression, span) not in identified_expressions:
                    identified_expressions.append((expression, span))

        return identified_expressions


if __name__ == '__main__':

    reportScraper = ReportScraper()
    output = reportScraper.extract_metadata(report_type, report_id)

    pprint.PrettyPrinter(indent = 4).pprint(output)














    

