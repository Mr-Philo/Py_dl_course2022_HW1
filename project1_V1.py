import requests
from bs4 import BeautifulSoup

TEST_STR = ["Houqiang Li"]
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

pub_link_data = []

curr_year = 0
for child in pub_list_raw.children:
    if 'year' in child.get('class'):
        # Debug: In dblp serch web, year will be singally shown in the contents, so must be judged independentlly  2022.3.27
        continue
    else:
        for content_item in child.contents:
            class_of_content_item = content_item.attrs.get('class', [0])
            if 'publ' in class_of_content_item:     # Debug: Here we need to judge wether the kind of the item is 'publication'  2022.3.27
                link = content_item.contents[0].find('a').attrs.get('href', "nothing")
                # print(link)
                pub_link_data.append(link)      # add data to list
# anaylise data part passed

for item in pub_link_data:
    print(item)
