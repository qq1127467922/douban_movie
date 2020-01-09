import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
data = pd.read_csv('国家和关键词数据.csv')
def area(string):
    return string.strip().split('/')[0].strip()#提取国家信息
#获取每个国家的关键词
def area_comment(area_name):
    return data[data['area']==area_name]
#改中国名字
def name(string):
    string = '中国'
    return string
def key_word_count(area_name):
    data = area_comment(area_name)
    string_key = ''
    for word in data['key_word']:
        string_key = string_key + word
    list_key = string_key.split(' ')
    series_key = pd.DataFrame({'key_word':list_key})
    count = series_key.groupby(['key_word'], as_index=False)['key_word'].agg({'cnt': 'count'})#统计关键词词频
    key_word = count['key_word']#关键词
    key_count = count['cnt']#词频
    image = np.array(Image.open('./地图/'+area_name+'.jpeg'))#导入背景国家地图
    wordcloud = WordCloud(scale= 12,
                          mask=image,
                          background_color='white',
                          font_path="./SimHei.ttf"
                          ).generate(string_key)#词云
    plt.imshow(wordcloud,interpolation="bilinear")
    plt.savefig('./img/'+area_name+'关键词词云'+".jpg", dpi=800)#保存词云图片
if __name__ == '__main__':
    data['area'] = data['area'].apply(area)
    count = data.groupby(['area'], as_index=False)['area'].agg({'cnt': 'count'})
    area_list = list(count['area'])  # 国家列表
    area_list.remove('中国台湾')
    area_list.remove('中国大陆')
    area_list.remove('中国香港')
    area_list.append('中国')
    print(area_list)
    United_States = data[data['area'] == '美国']  # 美国评论
    China = data.loc[(data['area'] == '中国台湾') | (data['area'] == '中国大陆') | (data['area'] == '中国香港')]  # 中国评论
    China['area'] = China['area'].apply(name)
    for area_name in area_list:
        if area_name == '中国':
            data = China#中国评论
            string_key = ''
            for word in data['key_word']:
                string_key = string_key + word
            list_key = string_key.split(' ')
            series_key = pd.DataFrame({'key_word': list_key})
            count = series_key.groupby(['key_word'], as_index=False)['key_word'].agg({'cnt': 'count'})
            key_word = count['key_word']
            key_count = count['cnt']
            image = np.array(Image.open('./地图/'+area_name + '.jpeg'))
            wordcloud = WordCloud(mask=image,
                                  font_path="SimHei.ttf").generate(
                string_key)
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.savefig('./img/' + area_name + '关键词词云' + ".jpg")
        key_word_count(area_name)
