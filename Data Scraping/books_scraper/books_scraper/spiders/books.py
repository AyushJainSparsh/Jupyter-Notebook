import scrapy
import pandas as pd


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
         #print(list(response.css("a")))
        '''link_href=[]
        for link in response.css("a"):
            #print("link ",link.attrib["href"])
            link_href.append(link.attrib["href"])
        return {"link ": link_href}
        '''
        link_href=[]
        for blink in response.css("ol.row article.product_pod a"):
            #print("Book link ",blink.attrib["href"])
            yield response.follow(blink.attrib["href"] , callback = self.extract_book)
        for next_page in response.css("ul.pager li.next a"):
            #print("Next Page link ",next_page.attrib["href"])
            yield response.follow(next_page.attrib["href"] , callback = self.parse)
        #return {"link ": link_href}

    def extract_book(self,response):
        title=response.css("div.product_main h1::text").get()
        price=response.css("div.product_main p.price_color::text").get()
        description=response.css("#product_description + p::text").get()
        table_info=response.css("table.table").get()
        book_info=pd.read_html(table_info)[0].set_index(0).to_dict()[1]
        book_info["title"]=title
        book_info["price"]=price
        book_info["description"]=description
        return book_info

