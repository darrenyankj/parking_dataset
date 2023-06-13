import scrapy


class ParkingscraperSpider(scrapy.Spider):
    name = "parkingscraper"
    allowed_domains = ["onemotoring.lta.gov.sg"]
    #start_urls = ["https://onemotoring.lta.gov.sg/content/onemotoring/home/owning/ongoing-car-costs/parking/parking_rates.1.html"]

    def start_requests(self):
        yield scrapy.Request(url = 'https://onemotoring.lta.gov.sg/content/onemotoring/home/owning/ongoing-car-costs/parking/parking_rates.1.html', callback = self.parse,
                             meta = {'Page': 'Orchard'},
                             headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'})

    def parse(self, response):
        table = response.xpath('//table[@class="parking_rate"]')

        final_header = []
        table_header = table.xpath('./thead/tr/th')
        for header in table_header:
            head = "".join(header.xpath('./text()').extract())
            final_header.append(head)

        yield {
            'page': response.request.meta['Page'],
            'header': final_header
        }

        table_body = table.xpath('./tbody/tr')

        for table_row in table_body:
            row_data = table_row.xpath('./td/text()').getall()

            yield {
                'page': response.request.meta['Page'],
                'body': row_data
            }

        pages = response.xpath('//select/option')
        for page in pages:
            site = page.xpath('./@value').get()
            site_name = page.xpath('./text()').get()
            yield scrapy.Request(url = f'https://onemotoring.lta.gov.sg{site}', callback = self.parse,
                                meta = {'Page': site_name},
                                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'})

        





