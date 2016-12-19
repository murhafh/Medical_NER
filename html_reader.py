# This class is used to read NHS pages and return the relevant text only

from bs4 import BeautifulSoup
import urllib2
import re

class HTMLReader(object):
    def __init__(self, url =''):
        self.url = url
        self.headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        
    def get_text_from_page(self):
        request = urllib2.Request(self.url, None, self.headers)
        response = urllib2.urlopen(request)

        html = response.read()

        html_dom =  BeautifulSoup(html)
        # get main content div
        content_div = html_dom.find("div", { "class" : "main-content healthaz-content clear" })
        # remove irrelevant divs
        content_div.find('div', id="webZoneMiddleTop").decompose()
        content_div.find('div', { "class" : "review-dates" }).decompose()
        cleaned_text = re.sub('\n\n', '', content_div.text)
        # List items end up having two spaces, replace that with a comma
        cleaned_text = re.sub('  ', ', ', cleaned_text)
        
        return cleaned_text
