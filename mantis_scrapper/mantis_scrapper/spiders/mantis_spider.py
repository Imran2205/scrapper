import scrapy
import json


class MantisSpider(scrapy.Spider):
    name = "scraper"

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
        filename = f'{self.name}_{page.lower()}_table_data.json'
        device_summary_divs = response.css('div.device-summary-container')
        device_summary_tables = device_summary_divs.css('div.device-summary-table')
        table_dict = {}
        for table in device_summary_tables:
            tab_head = table.css('h6::text')[0].get()
            print('************************************', tab_head)

            keys = table.css('span.label')
            values = table.css('span.label-value')

            table_dict[tab_head] = {}
            for i, key in enumerate(keys):
                key_span = key
                val_span = values[i]

                # print(key_span, '||', key_span.xpath("./*").get())
                # print(val_span.get(), '||', key_span.xpath("./*").get())

                key_val = self.get_text_from_span(key_span)
                val_val = self.get_text_from_span(val_span)

                table_dict[tab_head][key_val] = val_val

                print(key_val, ':', val_val)

            print('#########################################################################', len(keys), len(values))

        violations_div = response.css('div.ag-center-cols-container')

        violation_rows = violations_div.css('div.ag-row')

        print("***************************************************************************")
        table_dict['Violations'] = {}
        for r_c, row in enumerate(violation_rows):
            check = row.css('div[col-id="check"]::text').get().replace('\n', '')
            review = row.css('div[col-id="reviews"]::text').get().replace('\n', '')
            e_cell_val = row.css('span[ref="eCellValue"]::text').get().replace('\n', '')
            hier = row.css('div[col-id="hier_error_count"]::text').get().replace('\n', '')
            table_dict['Violations'][f"{r_c}"] = {
                'e_cell_value': e_cell_val,
                'check': check,
                'review': review,
                'hier_error_count': hier
            }
            print(e_cell_val, '||', review, '||', check, '||', hier)
        print("***************************************************************************")

        with open(f'{filename}', 'w') as f:
            json.dump(table_dict, f, indent=4)

        self.log(f'Saved file {filename}')


# scrapy crawl scraper