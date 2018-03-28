import urllib.request
import argparse
from bs4 import BeautifulSoup
import html2text
import lxml
import requests
import constant

constant.IMG_BASE_URL = 'https://github.com/nineyang/blog-tool/blob/master/'


def main(main_url):
    """

    :param main_url:
    :return:
    """
    main = spider(main_url)
    soup = BeautifulSoup(main, "lxml")
    # 确定页码
    total_page = soup.find('li', class_='next').previous_sibling.string
    for i in range(int(total_page)):
        handlerPage(i + 1)


# 确定详情页的格式

# 讲图片转到本地来


def spider(url):
    """
    :param url:
    :return:
    """
    headers = {
        'User_Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    return response.read().decode('utf-8')


def handlerPage(page):
    """
    处理列表页码
    :param page:
    :return:
    """
    list_page = 'https://www.hellonine.top/index.php/page/' + str(page)
    result = spider(list_page)
    soup = BeautifulSoup(result, "lxml")
    # 确定详情页面
    list = soup.find_all('div', class_='item-title')
    for link in list:
        handlerDetail(link.a['href'])


def handlerDetail(url):
    result = spider(url)
    soup = BeautifulSoup(result, "lxml")
    title = soup.find('h1', {'class', 'post-title'}).string.strip()
    content = soup.find('div', class_="post-content")
    content.find('p', class_="post-tags").extract()
    # 如果有图片的话，处理图片，下载图片存到本地
    img_list = content.find_all('img')
    for img in img_list:
        if img['src'].find("hellonine.top") != -1:
            image = requests.get(img['src'])
            if image.status_code == 200:
                file = "images/" + img['alt']
                open(file, 'wb').write(image.content)
                img['src'] = constant.IMG_BASE_URL + file
    article = html2text.html2text(str(content))
    open('blogs/' + title + '.md', 'w').write(article)
    exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-url', required=True, help='spider url')
    args = parser.parse_args()
    handlerDetail("https://www.hellonine.top/index.php/archives/93/")
    # main(args.url)
