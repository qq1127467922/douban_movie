import thulac
import math
import pandas as pd
stopwords_path = './stopwords.txt'
stopwords = []
for line in open(stopwords_path):
    stopwords.append(line.strip())
lac = thulac.thulac(seg_only=True)#分词
words_df = {}
cnt = 0
data = pd.read_csv('./top250_result.csv')
list_word = []
word_count = {}
for line in data['comment']:
    word_count = {}
    words_df = {}
    words = lac.cut(line.strip())
    article_vocab = []
    for word_tuple in words:
        word = word_tuple[0]
        word = word.strip()
        if word in stopwords:
            continue
        if word in article_vocab:
            continue
        article_vocab.append(word)
    for word in article_vocab:
        if word not in words_df:
            words_df[word] = 1
        else:
            words_df[word] += 1
    cnt += 1
    output_dict = {}
    string_word = ' '
    count = 0
    for word,rest in words_df.items():#便利词典
        output_dict[word] = rest
    for word,df in sorted(output_dict.items(),key=lambda d:d[1],reverse=True):#排序
        word_count[word] = df#词频
    total_docs = 0
    first_line_flag = True
    words_tfidf = {}
    string_word = ' '
    for word,tf in word_count.items():
        if word not in word_count:
            word_count[word]=5
        words_tfidf[word]=float(tf) * math.log(total_docs/word_count[word] + 1)
    ii = 0
    for word,tfidf in sorted(words_tfidf.items(),key=lambda d:d[1],reverse=True)[:21]:#２０个关键词
        if ii < 21: #20个关键词
            string_word = string_word + ' ' + word
            ii += 1
    list_word.append(string_word)
    print(string_word)
    string_word = ' '
area_data = data['area']
dict_ = pd.DataFrame({'area':area_data,'key_word':list_word})#保存国家和关键词信息
dict_.to_csv('./国家和关键词数据.csv')