# _*_ coding:utf-8 _*_
import pkuseg
import json
from ...common import merge_synonym


seg = pkuseg.pkuseg('D:\python\Lib\site-packages\pkuseg\default_v2')  # 开启词性标注功能
filename_input = '../../../lab1_stage1/movie_spider/doc/json/info_movie.json'
filename_output = '../doc/words_movies.json'
filename_stopwords = '../doc/stop_words_movies.json'
words_set = []
with open(filename_input, encoding='UTF-8') as f_info:  # 加上encoding参数，否则会解码报错
    info = json.load(f_info)
with open(filename_stopwords, encoding='UTF-8') as f_stopwords:
    stop_words = json.load(f_stopwords)

for film_id in range(0, len(info)):
    plot = seg.cut(info[film_id]["剧情简介"].replace("\\par", ""))  # 进行分词
    titles = info[film_id]["基本信息"]["标题"].split()
    casts = []
    for actor in info[film_id]["演职员"]:
        casts.append(actor[0])
        casts.extend(actor[1].split())
    key_words = titles + info[film_id]["基本信息"]["类型"] + casts + plot
    key_words_temp = key_words[:]
    for member in key_words_temp:  # 去除停用词
        if member in stop_words:
            key_words.remove(member)

    merged_keywords = []
    for word in key_words:  # 合并相同的词
        if word not in merged_keywords:
            merged_keywords.append(word)

    print(merged_keywords)
    words_set.append(merged_keywords)

print(len(words_set))
with open(filename_output, 'w', encoding="UTF-8") as f_output:  # 以写入模式打开文件
    json.dump(words_set, f_output, ensure_ascii=False, indent=4)  # 中文的写入 json.dump需要加上ensure_ascii=False
    # 参数。否则默认写入unicode;
    # 若觉得每一行太长可以在最后加上indent=4参数
