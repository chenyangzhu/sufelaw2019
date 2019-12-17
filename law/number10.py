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

def getn(string):
    words = pseg.cut(string)
    name = []
    for word, flag in words:
        if flag == 'n':  # 人名词性为nr
            name.append(word)
    return(''.join(name))

def ADBinfo(data, index):
    info = {}
    info['原告'] = []
    info['被告'] = []

    accuser_tag = re.compile(r'原告|上诉人|申请人')
    defender_tag = re.compile(r'被告|被上诉人|被申请人')
    l1 = re.split(defender_tag, data['当事人'][index])  # 840 844

    proxy = re.compile(r'代理人(.*)')
    legal = re.compile(r'代表人(.*)')
    location = re.compile(r'住所地(.*)|住(.*)|地(.*)|地址(.*)')
    gender = re.compile("男|女")
    date_born = re.compile(r'\d+年\d+月\d+日')
    ethic = re.compile(r'族$')

    a_ind = 0
    d_ind = 0

    for mes in l1:
        mes = re.sub(":", "", mes)
        l2 = re.split("。、", mes)

        # 有一定的结构层次， 但是依然很混乱“、” 分割每个个体的信息 “，”分割个体的属性
        # 有三种关系
        # 原告 被告
        # 上诉人 被上诉人
        # 申请人 被申请人
        # 先把再审信息放在备注

        flag = 0
        a = re.search(accuser_tag, mes)
        if a is not None: #1 表示原告信息
            flag = 1
            person = {}
        else:            #2 表示被告信息
            flag = 2
            person = {}

        for i in range(len(l2)):

            p = re.search(proxy, l2[i])
            le = re.search(legal, l2[i])
            p_gender = re.findall(gender, l2[i]) #提取性别
            p_birth = re.findall(date_born, l2[i])#提取出生日期
            p_location = re.findall(location, l2[i])#提取地址

            if len(p_gender) > 0:
                person['性别'] = ''.join(p_gender)
            if len(p_birth) > 0:
                person['出生年月'] = ''.join(p_birth)
            if len(p_location) > 0:
                person['地址'] = ''.join(list(filter(lambda s: s is not '', p_location[0])))

            leth = re.split("，", l2[i]) #提取民族
            for etho in leth:
                if re.search(ethic, etho) is not None:
                    person['民族'] = ''.join(etho)
            #委托/诉讼代理人 信息
            if p is not None:
                l4 = re.split("，", l2[i])
                person['委托/诉讼代理人'] = ''.join(re.findall(proxy, l4[0]))
                del (l4[0])
                if len(l4) > 0:
                    person['委托/诉讼代理人公司/职位'] = ''.join(l4)
            # 法定代表人 信息
            if le is not None:
                l4 = re.split("，", l2[i])
                person['法定代表人'] = ''.join(re.findall(legal, l4[0]))
                del (l4[0])
                if len(l4) > 0:
                    person['法定代表人职位'] = getn(''.join(l4))

            if flag is 1:
                person['序号'] = a_ind
                info['原告'].append(person)
                flag = 0
                a_ind = a_ind + 1

            if flag is 2:
                person['序号'] = d_ind
                info['被告'].append(person)
                flag = 0
                d_ind = d_ind + 1

    return (info)


def number10(data):
    data_len = len(data)
    information = []
    for i in range(data_len):
        # 显示进度
        if i % 100 == 0:
            print(i)
        info = {}
         #判断是否缺失 很重要
        if pd.isna(data['当事人'][i]):
           information.append(info)
           information.append({}) #空集合
           continue

        information.append(ADBinfo(data, i))

    return (information)  # return a new pandas DataFrame

basicinfomation = number10(data)
file=open('/Users/bailujia/Desktop/NLP/basicinfomation.txt','w')
file.write(str(basicinfomation));
file.close()