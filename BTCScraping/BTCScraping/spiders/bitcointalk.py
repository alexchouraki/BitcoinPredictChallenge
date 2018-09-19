
import scrapy


class BitcointalkSpider(scrapy.Spider):

    name = "bitcointalk"

    def start_requests(self):
        urls = [
            'https://bitcointalk.org/index.php?topic=3809457.00',
            ]
        for url in urls:
            yield scrapy.Request(url = url, callback = self.parse)


    def parse(self, response):
        identifier = str(response.xpath('//form/table').css('tr')[0].extract().split('class')[1][2:-6])

        for post in response.css('tr.'+identifier):
            try:
                yield {
                    'text': post.css('div.post::text').extract(),
                    'author_activity': post.css('div.smalltext')[0].css('div::text').extract()[3].split('Activity: ')[1],
                    'author_merit':  post.css('div.smalltext')[0].css('div::text').extract()[4].split('Merit: ')[1],
                    'time' : post.css('div.smalltext')[1].css('div::text').extract(),
                    'topic': response.css('title::text').extract()
                 }
            except Exception as e:
                yield {
                    'text': post.css('div.post::text').extract(),
                    'author_activity': 'NA',
                    'author_merit':  'NA',
                    'time' : post.css('div.smalltext')[1].css('div::text').extract(),
                    'topic': response.css('title::text').extract()
                }
        
        next_page = response.css('span.prevnext')[1].css('a::attr("href")').extract()[0]
        if next_page != None:
            next_page = response.css('span.prevnext')[1].css('a::attr("href")').extract()[0]
            yield response.follow(next_page, self.parse)