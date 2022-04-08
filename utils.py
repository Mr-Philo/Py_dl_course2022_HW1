import requests
from bs4 import BeautifulSoup

TEST_STR = ["Yaqin Zhang"]
DBLP_BASE_URL = 'https://dblp.org/'
SEARCH_URL = DBLP_BASE_URL + "search/"

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
    Chrome/55.0.2883.87 Safari/537.36'
}


def get_pub_data(pub):

    ptype, link, authors, title, where = '', '', [], '', ''

    if 'year' in pub.get('class'):
        # Debug: In dblp serch web, year will be singally shown in the contents, so must be judged independentlly  2022.3.27
        # continue
        return int(pub.contents[0])  # provide following criteria
    else:
        ptype = pub.attrs.get('class')[1]  # 'Type' can be judged bufore we judge the class of the item
        for content_item in pub.contents:
            class_of_content_item = content_item.attrs.get('class', [0])
            if 'data' in class_of_content_item:
                for author in content_item.findAll('span', attrs={"itemprop": "author"}):
                    authors.append(author.text)
                title = content_item.find('span', attrs={"class": "title"}).text
                for where_data in content_item.findAll('span', attrs={"itemprop": "isPartOf"}):
                    found_where = where_data.find('span', attrs={"itemprop": "name"})
                    if found_where:
                        where = found_where.text
            if 'publ' in class_of_content_item:  # Debug: Here we need to judge wether the kind of the item is 'publication'  2022.3.27
                link = content_item.contents[0].find('a').attrs.get('href', "nothing")
    return {'Type': ptype, 'Link': link, 'Authors': authors, 'Title': title, 'Where': where}  # Create data structure: Dictionary


class HtmlCrawler(object):

    # Debug 2022/4/4: When writing functions in class, we should add param "self" in each fuction
    def Crawl_html(self, key=TEST_STR):      # if input param is none, we use TEST_STR defaultly
        soup = BeautifulSoup(
            requests.get(SEARCH_URL, params={'q': key}).content, "html.parser")
        pub_list_raw = soup.find("ul", attrs={"class": "publ-list"})
        return pub_list_raw


class HtmlParser(object):

    def Parse_html(self, pub_list_raw):
        pub_list_data = []  # the list of dictionaries

        curr_year = 0
        for child in pub_list_raw.children:
            pub_data = get_pub_data(child)
            # pub_list_data.append(pub_data)
            if type(pub_data) == int:  # Debug: To follow the rule of dblp serch web  2022.3.29
                curr_year = pub_data
            else:
                pub_data['Year'] = curr_year
                pub_list_data.append(pub_data)

        return pub_list_data


class Outputer(object):

    # def output_terminal(self, datas):  # see results on terminal
    #     print("------------------------------------------------------------------------------------------------------------------------------------------")
    #     print("|  Type  |                  Link                  |  First Author  |                          Title                             |  year  |")
    #     for item in datas:
    #         if item.get('Link') == '':
    #             continue
    #         print("------------------------------------------------------------------------------------------------------------------------------------------")
    #         print("|{:^8}|{:^40}|{:^16}|{:^60}|{:^8}|".format(item.get('Type'),
    #                                                           item.get('Link'),
    #                                                           (item.get('Authors')[0] if len(item.get('Authors')) else ''),
    #                                                           item.get('Title'),
    #                                                           item.get('Year')))
    #     print("------------------------------------------------------------------------------------------------------------------------------------------")
    def output_terminal(self, datas):      # simple terminal output
        print("\nAll related publications links are listed as belows:")
        for item in datas:
            if item.get('Link') == '':
                continue
            print(item.get('Link'))
        print("For more details, please refer the document \"result.html\" in web page.\n")

    def outputer_html(self, datas, search_str):

        f = open("result.html", "w", encoding='utf-8')

        f.write('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>DBLP Searching Information</title>
        </head>
        ''')

        f.write("<body>\n")
        f.write("<table border='1' width='100%' cellspacing='0' cellpadding='4' bgcolor='#EEF7F2'>\n")
        f.write("<caption><h3>Searching Result for \"%s\"</h3></caption>\n" % search_str)
        f.write('''
        <tr>
            <th>Type</th>
            <th>Link</th>
            <th>First Author</th>
            <th>Title</th>
            <th>Source</th>
            <th>Year</th>
        </tr>
        ''')
        for item in datas:
            if item.get('Link') == '':
                continue
            f.write("<tr>\n")
            f.write("   <td>{}</td>\n".format(item.get('Type')))
            f.write("   <td><a href='{}'>{}</a></td>\n".format(item.get('Link'), item.get('Link')))
            f.write("   <td><a href='{}'>{}</a></td>\n".format(("https://dblp.org/search?q=" + item.get('Authors')[0]), item.get('Authors')[0] if len(item.get('Authors')) else ''))
            f.write("   <td>{}</td>\n".format(item.get('Title')))
            f.write("   <td>{}</td>\n".format(item.get('Where')))
            f.write("   <td>{}</td>\n".format(item.get('Year')))
            f.write("</tr>\n")

        f.write("</table>\n")

        f.write("<br/>")
        f.write("<div align='right'>Note: The data shown above is from <a href='https://dblp.org/'>https://dblp.org/</a> </div>\n")
        f.write("<div align='right'>For py_dl_course2022 larning only    --Ruizhe Wang </div>\n")
        f.write("</body>\n")
        f.write("</html>\n")
        f.close()
