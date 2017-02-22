import scrapy
from dmsims.items import DmsimsItem

class DmozSpider(scrapy.Spider):
    name = 'dmsims'
    start_urls = ['http://files.pinoypercussionfreaks.com/']

    def parse(self, response):
        links = response.css('ul > li > article > a::attr("href")')
        for href in links:
            url = response.urljoin(href.extract())
            yield scrapy.Request(response.urljoin(url), self.parse_dl_page)

        next_page = response.css('.nextpostslink::attr("href")')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

    def parse_dl_page(self, response):
        title = response.css('title').extract()
        link = response.css('a.simfile-download-button::attr("href")').extract()
        item = DmsimsItem()
        item['title'] = response.xpath('//title/text()').extract()
        item['link'] = link
        yield item
