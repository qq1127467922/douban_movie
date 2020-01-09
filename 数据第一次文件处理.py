import pandas as pd
data = pd.read_csv('./250top电影.csv')
df_comment = data['movie_comment']#获取电影评论信息
list1 = []#新的评论
string = ''
for i in range(len(df_comment)):#拼接评论
    print(i)
    if (i+1) % 10 == 0 or i== 1671:
        string = string + df_comment[i]
        list1.append(string)
        string = ''
    else :
        string = string + df_comment[i]
data = data[['movie_name','movie_area','movie_year','movie_dir']]
data = data.drop_duplicates()#去重
df_dir = data['movie_dir'].values#导演
df_time = data['movie_year'].values#年份
df_area = data['movie_area'].values#国家
df_name = data['movie_name'].values#片名
print(len(df_name),len(df_area),len(df_time),len(df_dir),len(list1))
dict_ = pd.DataFrame({'name':df_name,'dir':df_dir,'time':df_time,'area':df_area,'comment':list1})
dict_.to_csv('top250_result.csv')

