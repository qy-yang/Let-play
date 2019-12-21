import re
import os
from datetime import datetime
from pathlib import Path
import traceback

import scrapy
from bs4 import BeautifulSoup
from sina.items import SinaItem


class SinaNewsSpider(scrapy.Spider):
    name = "sina_news"
    with open(os.path.join(Path(__file__).parent, 'urls.txt')) as f:
        start_urls = f.readlines()
    custom_settings = {'LOG_LEVEL': 'ERROR'}
    
    # def start_requests(self):
    #     urls = [
    #         'https://news.sina.com.cn/'
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        tags = soup.find_all('a', href=re.compile('(?=^http.*sina.*\d{4}-\d{2}-\d{2}.*html$)'))
        for tag in tags:
            url = tag.get('href')
            yield scrapy.Request(url, callback=self.parse_details)

    def parse_details(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            title = self.extract_title(soup)
            if not title:
                raise Exception('Skip ' + response.url + ' cannot find the title.')
            content = self.extract_content(soup)
            if not content:
                raise Exception('Skip ' + response.url + ' cannot find the content.')
            print(title)
        except Exception as e:
            self.logger.error(str(e))
            self.logger.error(traceback.format_exc())
        item = SinaItem(_id=response.url, title=title, content=content)
        yield item
    @staticmethod
    def extract_title(soup):
        selectors = ['h1.main-title', 'h1.l_tit', '#artibodyTitle',
                     'h1#main_title', 'h1.title', 'div.catuncle-title h1',
                     'div.article-header h1', 'div.titleArea h1',
                     'span.location h1', 'h4.title', 'div.crticalcontent h1 span',
                     'div.news_text h1', 'h1.art_tit_h1', 'div.conleft_h1 h1',
                     'h1.m-atc-title', 'div.b_txt h1 a']
        for selector in selectors:
            if len(soup.select(selector)) != 0:
                return soup.select(selector)[0].text.strip()
        # if none of selector matches the title, try to find from meta header info
        if soup.title and soup.title.string.strip():
            return soup.title.string.strip()

    @staticmethod
    def extract_content(soup):
        selectors = ['div.article p', 'div#artibody p', 'div.mainContent p',
                     'div.article-body p', 'div#editHTML p', 'div.article-content p',
                     'div.l_articleBody p', 'div.catuncle-p p',
                     'div#artibody div p', 'div#articleContent p',
                     'div#fonttext p', 'div.pingcetext p',
                     'div.s_infor p', 'div.fonttext p']
        for selector in selectors:
            if len(soup.select(selector)) !=0:
                return '\n'.join([p.text for p in soup.select(selector)])