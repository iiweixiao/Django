import time
import random
import requests
from lxml import etree

# from app01.models import SougouNewsInfo


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44',
}


def parse_html(url):
    """返回一个列表data_list，用于存储多个字典数据：搜狗资讯的title,href,source,created"""
    resp = requests.get(url, headers=headers)
    html = etree.HTML(resp.text)
    div_list = html.xpath('//*[@class="vrwrap"]')
    data_list = []
    for i in div_list:
        # 拿到a标签及a标签内em标签的文字，['2022年报考','一建',',哪些地区需要社保?']
        title = i.xpath('./div/h3/a//text()')
        title = ''.join(title)  # 合并文字
        if title.strip() == '':
            title = '抓取失败'
            continue
        try:
            href = i.xpath('./div/h3/a/@href')[0]
            href = 'https://www.sogou.com' + href
        except:
            href = ''
        try:
            source_from = i.xpath('./div/div//div/p/span[1]/text()')[0]
            created = i.xpath('./div/div//div/p/span[2]/text()')[0]
        except:
            source_from = ' '
            created = ' '
        div_dict = {'title': title, 'href': href, 'source_from': source_from, 'created': created}
        data_list.append(div_dict)
    return data_list


# 爬取关键词列表中每个关键词，默认爬取1页
def sougou(key_words, page=1):
    content = ''
    index = 1
    html_query = []
    for key_word in key_words:
        for i in range(page):
            # 搜狗搜索的资讯频道
            url = f'https://www.sogou.com/sogou?interation=1728053249&query={key_word}&page={i}'
            data_list = parse_html(url)
            for div_dict in data_list:
                print(index, div_dict['title'], div_dict['source_from'], div_dict['created'], div_dict['href'])
                title = div_dict['title']
                source_from = div_dict['source_from']
                created = div_dict['created']
                href = div_dict['href']
                # SougouNewsInfo.objects.create(title=title, href=href, source=source_from, created=created)
                content += f"{index} <a href='{href}'>{title}</a> <br>{source_from} {created} <br> <br>"
                html_data = {}
                html_data['index'] = index
                html_data['title'] = title
                html_data['href'] = href
                html_data['source_from'] = source_from
                html_data['created'] = created
                html_query.append(html_data)
                index += 1
            time.sleep(random.random())

    return content, html_query


if __name__ == '__main__':
    key_words = ['小牛', '华为']
    info = '资讯_from搜狗搜索'
    sougou(key_words, 2)
    # send_email('weixiaot2021@icloud.com', sougou(key_words), info)
    # send_email('gaoming595@sina.com', sougou(key_words), info)
    # send_email('iiweixiao@yeah.net', sougou(key_words), info)
