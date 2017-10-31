# -*- coding: utf-8 -*-
import scrapy


class AuthorDetailsSpider(scrapy.Spider):
    name = "Author_Details"
    allowed_domains = ["toscrape.com"]
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        self.log("I just visited"+response.url)
        urls = response.css("div.quote > span > a::attr(href)").extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.parse_detail)
           
        next_url = response.css("li.next > a::attr(href)").extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url = next_url, callback=self.parse)
            
            
    def parse_detail(self, response):
        author ={
            'Name':response.css("h3.author-title::text").extract_first(),
            'Birth_date':response.css("span.author-born-date::text").extract_first(),
        }
        yield author
