import scrapy
import json
from ..items import BookItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['antispider7.scrape.center']
    start_urls = 'http://antispider7.scrape.center'
    max_page = 512

    def start_requests(self):
        for page in range(1, self.max_page + 1):
            url = f'{self.start_urls}/api/book/?limit=18&offset={(page - 1) * 18}'
            yield scrapy.Request(url, callback=self.parse_index)

    def parse_index(self, response):
        data = json.loads(response.text)
        results = data.get('results', [])
        for result in results:
            id = result.get('id')
            url = f'{self.start_urls}/api/book/{id}/'
            yield scrapy.Request(url, callback=self.parse_detail, priority=2)

        """
{id: "7952978", name: "Wonder", authors: ["R. J. Palacio"],…}
authors: ["R. J. Palacio"]
cover: "https://img1.doubanio.com/view/subject/l/public/s27252687.jpg"
id: "7952978"
name: "Wonder"
score: "8.8"
1: {id: "7916054", name: "清白家风", authors: ["↵ 董桥", "海豚简装"],…}
        """

    def parse_detail(self, response):
        data = json.loads(response.text)
        item = BookItem()
        for field in item.fields:
            item[field] = data.get(field)
        yield item




