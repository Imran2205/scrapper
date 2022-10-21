import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'file://C:/Users/admin/Desktop/desktop/web/scrapper/html/Mantis.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        filename = f'quotes-{page}.html'

        violations_div = response.css('div.ag-center-cols-container')

        violation_rows = violations_div.css('div.ag-row')

        print("***************************************************************************")

        for r_c, row in enumerate(violation_rows):
            check = row.css('div[col-id="check"]::text').get()
            review = row.css('div[col-id="reviews"]::text').get()
            e_cell_val = row.css('span[ref="eCellValue"]::text').get()
            hier = row.css('div[col-id="hier_error_count"]::text').get()
            print(e_cell_val, review, check, hier)
        print("***************************************************************************")