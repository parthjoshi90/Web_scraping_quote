# -*- coding: utf-8 -*-
import scrapy
import csv


class QuoteSpider(scrapy.Spider):
    name = "quote"
    allowed_domains = ["toscrape.com"]
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):     
        for author in response.css('div.quote'):
            thoughts = {
                'author':author.css("small.author::text").extract_first(),
                'quote':author.css("span.text::text").extract_first(),
                'tags':author.css("a.tag::text").extract(),
            }
            yield thoughts
        
        next_url = response.css("li.next > a::attr(href)").extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url = next_url, callback=self.parse)