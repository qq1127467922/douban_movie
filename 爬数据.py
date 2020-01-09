import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
headers = {
    'cookie':'bid=xiXasJy_T2s; ll="118304"; __yadk_uid=ucYJzWLxVGkxVUZzkLuOr2WKGYDQUChd; _vwo_uuid_v2=DDF040CDC39D506E32CB70680F68474E1|09b885503496bad5cd4ffc77a93035b1; trc_cookie_storage=taboola%2520global%253Auser-id%3Da50462e2-0a35-4fe0-8d41-70f031512552-tuct4efa694; __utmz=30149280.1576501815.5.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmz=223695111.1576501815.5.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1576580060%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_id.100001.4cf6=774b2f69656869fe.1576307574.6.1576580060.1576501818.; _pk_ses.100001.4cf6=*; ap_v=0,6.0; __utma=30149280.1798292817.1576307574.1576501815.1576580061.6; __utmb=30149280.0.10.1576580061; __utmc=30149280; __utma=223695111.844953453.1576307574.1576501815.1576580061.6; __utmb=223695111.0.10.1576580061; __utmc=223695111',
    'referer':'https://movie.douban.com/top250?start=0&filter=',
    'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}
list_name = []#存储电影名称
list_dir = []#存储电影导演
list_year = []#存储年份
list_area = []#存储地区
list_com = []#存储评论
for i in range(0,10):
    time.sleep(7)
    url = 'https://movie.douban.com/top250?start={0}&filter='.format(i*25)
    url_r = requests.get(url,headers=headers)#get请求网页
    url_b = BeautifulSoup(url_r.text,'lxml')#解析
    movie_list = url_b.find('ol',attrs={'class':'grid_view'})#电影列表
    #print(url_list)
    for movie_li in movie_list.find_all('li'):
        movie_url = movie_li.find('a').attrs['href']  # 获取电影链接
        time.sleep(6)
        movie_r = BeautifulSoup(requests.get(movie_url,headers=headers).text,'lxml')
        movie_name = movie_r.h1.span.string#获取h1中span的内容(电影标题)
        movie_directed = movie_r.find('a',rel='v:directedBy').string#电影导演
        time_ = movie_r.h1.find('span',class_='year').string#找到class为year的标签span的内容(年份)
        info_div = movie_r.find('div', attrs={'id': 'info'})
        for child in info_div.children:
            if child.string and child.string.startswith('制片国家/地区'):
                area = child.next_sibling.string.strip()#制片国家
                print(area)
        comment_url = movie_url+'reviews'#评论地址
        time.sleep(7)
        #print(url_)
        comment_req = BeautifulSoup(requests.get(comment_url, headers=headers).text, 'lxml')
        comment_id = comment_req.find_all('div',class_='review-short')
        for j in range(10):
            rid = comment_id[j].attrs['data-rid']
            rid_url = 'https://movie.douban.com/j/review/'+rid + '/full'
            time.sleep(5)
            requ = requests.get(rid_url,headers=headers)
            html = requ.json()['body']
            html = html.replace('<br>','')
            html = html.replace('<br/>', '')
            html = html.replace('</p>', '')
            html = html.replace('<p>', '')
            html = BeautifulSoup(html,'lxml')
            br = html.find('div',class_='review-content clearfix')
            comment = ' '
            comment = comment + br.get_text()
            print(comment)
            list_name.append(movie_name)
            list_dir.append(movie_directed)
            list_year.append(time_)
            list_area.append(area)
            list_com.append(comment)
dict_ = pd.DataFrame({'name': list_name, 'dir': list_dir, 'time': list_year,'area':list_area,'comment':list_com})
dict_.to_csv('top250电影.csv')#保存数据



