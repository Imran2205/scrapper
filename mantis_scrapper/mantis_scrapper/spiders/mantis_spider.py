import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'file://C:/Users/admin/Desktop/desktop/web/scrapper/html/Mantis.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def get_text_from_span(self, span_ele):
        ret_str = ""
        if span_ele.get().startswith('<span'):
            if span_ele.xpath("./*"):
                ret_str = self.get_text_from_span(span_ele.xpath("./*"))
            else:
                ret_str = span_ele.css('span::text').get()
        elif span_ele.get().startswith('<a'):
            a_tags = span_ele.css('a')
            for cnt, a in enumerate(a_tags):
                if cnt == 1 and len(a_tags) == 2:
                    ret_str += f" [{a.css('a::text').get()}]"
                else:
                    ret_str += a.css('a::text').get()
        elif span_ele.get().startswith('<input'):
            ret_str = span_ele.css('input::attr(value)').get()
        else:
            ret_str = span_ele.css('span::text').get()

        return ret_str

    def parse(self, response):
        print(response)
        page = response.url.split("/")[-1].split('.')[0]
        print('#########################################################################', page)
        filename = f'quotes-{page}.html'
        device_summary_divs = response.css('div.device-summary-container')
        device_summary_tables = device_summary_divs.css('div.device-summary-table')
        for table in device_summary_tables:
            tab_head = table.css('h6::text')[0].get()
            print('************************************', tab_head)

            keys = table.css('span.label')
            values = table.css('span.label-value')

            sub_table_dict = {}
            for i, key in enumerate(keys):
                key_span = key
                val_span = values[i]

                # print(key_span, '||', key_span.xpath("./*").get())
                # print(val_span.get(), '||', key_span.xpath("./*").get())

                key_val = self.get_text_from_span(key_span)
                val_val = self.get_text_from_span(val_span)

                print(key_val, ':', val_val)

            print('#########################################################################', len(keys), len(values))

        self.log(f'Saved file {filename}')
