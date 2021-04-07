import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import LlimestonebankItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class LlimestonebankSpider(scrapy.Spider):
	name = 'limestonebank'
	start_urls = ['https://www.limestonebank.com/about-us/news']

	def parse(self, response):

		articles = response.xpath('//div[@class="slider-hottopic-slide__inner"]')
		for article in articles:
			date = article.xpath('.//div[@class="content mb-3 card-date"]/div/text()').get().strip()
			post_links = article.xpath('.//p/a/@href').get()
			yield response.follow(post_links, self.parse_post, cb_kwargs=dict(date=date))

	def parse_post(self, response, date):
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="content pr-3 firsthead0m"]//text()[not (ancestor::h2)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=LlimestonebankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()


