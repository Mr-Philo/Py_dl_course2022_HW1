from utils import HtmlCrawler, HtmlParser, Outputer


# initial the web crawler
class My_Crawler(object):

    def __init__(self):
        self.crawler = HtmlCrawler()
        self.parser = HtmlParser()
        self.Outputer = Outputer()

    def craw(self, search_str):
        pub_list_raw = self.crawler.Crawl_html(search_str)      # Step 1: Crawl the web
        pub_list_data = self.parser.Parse_html(pub_list_raw)    # Step 2: Parse the web
        self.Outputer.output_terminal(pub_list_data)            # Step 3: Output for visibility
        self.Outputer.outputer_html(pub_list_data)


if __name__ == "__main__":
    search_str = "Houqiang Li"
    crawler = My_Crawler()
    crawler.craw(search_str)
