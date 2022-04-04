import requests
from bs4 import BeautifulSoup

TEST_STR = ["Machine Learning"]
DBLP_BASE_URL = 'https://dblp.org/'
SEARCH_URL = DBLP_BASE_URL + "search/"

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
Chrome/55.0.2883.87 Safari/537.36'
}

# test fuction: find all pubilicans of Houqiang Li
soup = BeautifulSoup(requests.get(SEARCH_URL, params={'q': TEST_STR}).content, "html.parser")
pub_list_raw = soup.find("ul", attrs={"class": "publ-list"})
# print(pub_list_raw)
# visit part passed


def get_pub_data(pub):

    ptype = ''
    link = ''
    authors = []
    title = ''
    where = ''

    if 'year' in pub.get('class'):
        # Debug: In dblp serch web, year will be singally shown in the contents, so must be judged independentlly  2022.3.27
        # continue
        return int(pub.contents[0])     # provide following criteria
    else:
        ptype = pub.attrs.get('class')[1]   # 'Type' can be judged bufore we judge the class of the item
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
            if 'publ' in class_of_content_item:     # Debug: Here we need to judge wether the kind of the item is 'publication'  2022.3.27
                link = content_item.contents[0].find('a').attrs.get('href', "nothing")
                # print(link)

    return {'Type': ptype,
            'Link': link,
            'Authors': authors,
            'Title': title,
            'Where': where}     # Create data structure: Dictionary
# anaylise data part passed


pub_list_data = []      # the list of dictionaries

curr_year = 0
for child in pub_list_raw.children:
    pub_data = get_pub_data(child)
    # pub_list_data.append(pub_data)
    if type(pub_data) == int:   # Debug: To follow the rule of dblp serch web  2022.3.29
        curr_year = pub_data
    else:
        pub_data['Year'] = curr_year
        pub_list_data.append(pub_data)


def print_result(list):     # see results on terminal
    print("------------------------------------------------------------------------------------------------------------------------------------------")
    print("|  Type  |                  Link                  |  First Author  |                          Title                             |  year  |")
    for item in list:
        if item.get('Link') == '':
            continue
        print("------------------------------------------------------------------------------------------------------------------------------------------")
        print("|{:^8}|{:^40}|{:^16}|{:^60}|{:^8}|".format(item.get('Type'),
                                                          item.get('Link'),
                                                          (item.get('Authors')[0] if len(item.get('Authors')) else ''),
                                                          item.get('Title'),
                                                          item.get('Year')))
    print("------------------------------------------------------------------------------------------------------------------------------------------")


print_result(pub_list_data)
