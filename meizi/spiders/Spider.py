from scrapy import Request
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from meizi.items import MeiziItem

class Meizi(CrawlSpider):
    name = 'meizi'
    allowed_domains = ['mzitu.com']
    start_urls = ['http://www.mzitu.com/']
    img_urls = []
    rules = (
        Rule(LinkExtractor(allow=('http://www.mzitu.com/\d{1,6}',), deny=('http://www.mzitu.com/\d{1,6}/\d{1,6}')),
             callback='parse_item', follow=True),
    )

    def parse_item(self,response):
        item = MeiziItem()
        # max_num 为页面最后一张图片的位置
        # /html/body/div[2]/div[1]/div[4]/a[5]/span
        max_num = response.xpath("descendant::div[@class='main']/div[@class='content']/div[@class='pagenavi']/a[last()-1]/span/text()").extract_first(default="N/A")
        item['name'] = response.xpath("./*//div[@class='main']/div[1]/h2/text()").extract_first(default="N/A")
        item['url'] = response.url
        for num in range(1, int(max_num)):
            # page_url 为每张图片所在的页面地址
            page_url = response.url + '/' + str(num)
            yield Request(page_url, callback=self.img_url)
        item['images_urls'] = self.img_urls
        print("*****************************************************************")
        print(item)
        yield item

    def img_url(self,response):
        img_urls = response.xpath("descendant::div[@class='main-image']/descendant::img/@src").extract()
        for img_url in img_urls:
            # 保存url
            self.img_urls.append(img_url)
