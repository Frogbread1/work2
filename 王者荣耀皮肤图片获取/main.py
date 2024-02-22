import requests
from lxml import etree
import os
import numpy as np
from time import sleep

#伪装
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 SLBrowser/9.0.3.1311 SLBChan/103'}

#访问英雄列表主页
hero_list_url = 'https://pvp.qq.com/web201605/js/herolist.json'
hero_list_resp = requests.get(hero_list_url,headers = headers)
for h in hero_list_resp.json():
    cname = h.get('cname') #获取英雄名称
    ename = h.get('ename') #获取英雄代码
    if not os.path.exists(cname):
        os.makedirs(cname) #用英雄名称创建存储皮肤图片的文件夹

    #访问英雄主页
    hero_info_url = f'https://pvp.qq.com/web201605/herodetail/{ename}.shtml'
    hero_info_resp = requests.get(hero_info_url,headers = headers)
    hero_info_resp.encoding = 'gbk' #使用国别体
    e = etree.HTML(hero_info_resp.text) #将网页的文本内容提取到pycharm中
    names = e.xpath('//ul[@class="pic-pf-list pic-pf-list3"]/@data-imgname')[0]
    names = [name[0:name.index('&')]for name in names.split('|')]

    #接收服务器响应
    for i,n in enumerate(names):
        resp = requests.get(f'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{ename}/{ename}-bigskin-{i+1}.jpg',headers= headers)
    # 保存
    with open(f'{cname}/{n}.jpg','wb') as f:
        f.write(resp.content)
    print(f'已下载{n}的皮肤')
    sleep(1)