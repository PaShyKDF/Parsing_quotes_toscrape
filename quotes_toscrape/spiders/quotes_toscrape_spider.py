import scrapy

from quotes_toscrape.items import QuotesToscrapeItem


class QuotesToscrapeSpiderSpider(scrapy.Spider):
    name = "quotes_toscrape_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for quote in response.css('div.quote'):
            data = {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('a.tag::text').getall(),
            }
            yield QuotesToscrapeItem(data)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
