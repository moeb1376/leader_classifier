# -*- coding: utf8 -*-
import scrapy
import re


class KhameneiSpider(scrapy.Spider):
    name = "khamenei"
    allowed_domains = ["farsi.khamenei.ir"]
    start_urls = [
        "http://farsi.khamenei.ir/speech?nt=2&year=1397",
    ]

    def parse(self, response):
        url = "http://farsi.khamenei.ir/speech?nt=%d&year=%d"
        nt, year = re.match(r'.*\?nt=(.)\&year=(.*)$', response.url, re.X).groups()
        nt = int(nt)
        year = int(year)
        for i in range(year, 1367, -1):
            request = scrapy.Request(url % (nt, i), callback=self.speech_link)
            request.meta['year'] = i
            yield request

    def speech_link(self, response):
        url = "http://farsi.khamenei.ir/print-content?id=%d"
        speech = response.xpath("//h2/a//@href").extract()
        for s in speech:
            id = re.match(r'.*\?id=(.*)$', s, re.X).groups()[0]
            id = int(id)
            request = scrapy.Request(url % id, callback=self.speech_content)
            request.meta['year'] = response.meta['year']
            yield request

    def speech_content(self, response):
        id = re.match(r'.*\?id=(.*)$', response.url, re.X).groups()[0]
        id = int(id)
        year = int(response.meta['year'])
        date = response.xpath("//span[@class='date']/text()").extract()[0]
        date = date.replace('/', '_')
        title = response.xpath("//h3[@class='title']/text()").extract()[0]
        content_with_p = response.xpath("//div[@class='content-box']/p")
        content_with_div = response.xpath("//div[@class='content-box']/div")
        content_withouth_div = response.xpath("//div[@class='content-box']")
        filename = 'data/%d/%d_%s.txt'
        if len(content_with_p) > len(content_with_div):
            content = ""
            for p in content_with_p:
                content += ''.join(p.xpath("text()").extract())
            with open(filename % (year, id, date), 'w') as f:
                f.write(content)
        elif len(content_with_div) > len(content_with_p):
            content = ""
            for div in content_with_div:
                content += ''.join(div.xpath("text()").extract())
            with open(filename % (year, id, date), 'w') as f:
                f.write(content)
        elif len(content_with_div) == 0 and len(content_with_p) == 0 and len(content_withouth_div) > 0:
            with open(filename % (year, id, date), 'w') as f:
                f.write(''.join(content_withouth_div.xpath("text()").extract()))
        else:
            with open("error_list.txt", 'a') as f:
                f.write(str(id))
            print("******%d******" % id, len(content_with_p), len(content_with_div))
