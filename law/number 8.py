import re
import numpy as np
import pandas as pd
import jieba.posseg as pseg
#import os
#import jieba

file_path = "/Users/bailujia/Desktop/NLP/IP01.xlsx"
alpha = 10
beta = 10
gamma = 10

# 读取一些数据
data = pd.read_excel(file_path)

def number8(data):
    # http://www.sohu.com/a/249531167_656612
    company = re.compile(r'.*?公司')
    data_len = len(data)
    natural_person = np.zeros(data_len)
    legal_person = np.zeros(data_len)
    other_person = np.zeros(data_len)
    for i in range(data_len):
        #显示进度
        if i % 100 == 0:
            print(i)
        #判断是否缺失
        if pd.isna(data['被告'][i]):
            continue
        #判断是否有字符串中是否有公司
        if re.search(company, data['被告'][i]) is not None:
            legal_person[i] = 1
        #查找名字：按标点分割后长度小于等于4，不含有公司（不考虑外国人和少数民族）
        l = re.split('、', data['被告'][i])
        l1 = list(filter(lambda s: len(s) <= 4, l))
        l2 = list(filter(lambda s: (re.search(company, s)) is None, l1))
        if len(l2) > 0:
            natural_person[i] = 1
        # 查找其他：按标点分割后长度大于4，不含有公司，且不含有谓语动词（数据有时会将起诉原因一并放入被告栏）
        l3 = list(filter(lambda s: len(s) > 4, l))
        l4 = list(filter(lambda s: (re.search(company, s)) is None, l3))
        if len(l4) > 0:
            other_person[i] = 1
            for mes in l4:
                words = pseg.cut(mes)
                verbs = []
                for word, flag in words:
                    if flag == 'v':  # 人名词性为nr
                        other_person[i] = 0
                        break

    data['被告_是否_自然人'] = natural_person
    data['被告_是否_法人'] = legal_person
    data['被告_是否_其他'] = other_person
    del natural_person, legal_person, other_person  # 控制内存

    return data  # return a new pandas DataFrame

number8(data)[['被告','被告_是否_自然人','被告_是否_法人','被告_是否_其他']].to_csv("/Users/bailujia/Desktop/NLP/tag.csv", index=False, sep=',',encoding='utf-8')
