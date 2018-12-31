# -*- coding: utf-8 -*-
import scrapy
import re


class RecrusulOnSpider(scrapy.Spider):
    name = 'recrusul_on'
    start_urls = ['http://cotacoes.economia.uol.com.br/acao/cotacoes-historicas.html?codigo=RCSL3.SA&beginDay=31&beginMonth=12&beginYear=2006&endDay=31&endMonth=12&endYear=2018&size=200&page=1&period=']

    def parse(self, response):

        for tr in response.css('.tblCotacoes tr'):
            yield {
                'date': '' + str(tr.css('td:nth-child(1)::text').extract_first()),
                'cotation': str(tr.css('td:nth-child(2)::text').extract_first()).replace(',', '.'),
                'minimum': str(tr.css('td:nth-child(3)::text').extract_first()).replace(',', '.'),
                'maximum': str(tr.css('td:nth-child(4)::text').extract_first()).replace(',', '.'),
                'value_variation': str(tr.css('td:nth-child(5)::text').extract_first()).replace(',', '.'),
                'volume': str(tr.css('td:nth-child(7)::text').extract_first()).replace('.', '').replace(',', '.')
            }

        links = response.css('.paginas').re('<li>.*</li>')
        len_links = len(response.css('.paginas').re('<li>.*</li>'))
        next_page = None
        if len_links > 1:

            for i in range(len_links):
                if re.compile(r'strong').search(links[i]):
                    if len_links-1 != i:
                        next_page = links[i + 1]
                        
        if next_page is not None:
            next_page = response.urljoin(next_page.replace("amp;", "").split('"')[1])
            yield scrapy.Request(next_page, callback=self.parse)
