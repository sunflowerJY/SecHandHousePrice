import requests as req
from bs4 import BeautifulSoup
import pandas as pd

def spiderSecHouse(addresslist, headers, houselist, cnt):
    for address in addresslist:
        print("开始抓取"+address+"区域的成交记录:")
        for i in range(1, 101):
            print("开始抓取" + address + "区域第"+str(i)+"页的成交记录:")
            if (i == 1):
                url = "https://sh.lianjia.com/chengjiao/" + address + "/p1p2p3/"
            else:
                url = "https://sh.lianjia.com/chengjiao/" + address + "/pg" + str(i) + "p1p2p3/"
            page = req.get(url, headers=headers)
            print(url + "页面状态码：{0}".format(page.status_code))
            soup = BeautifulSoup(page.text, "html.parser")

            listContent = soup.find_all(attrs={"class": "listContent"})
            ullist = listContent[0].find_all(name='li')

            if(len(ullist) == 0):
                print("该页内容为空，跳过")
                break
            for ul in ullist:
                print("已经爬取" + str(cnt)+"条二手房成交信息")
                cnt += 1
                infolist = ul.find_all(attrs={"class": "info"})
                # 小区、户型、面积
                alist = infolist[0].find_all(name='a')[0]
                split_titleinfo = alist.string.split(" ")
                if (len(split_titleinfo) == 3):
                    xiaoqu = split_titleinfo[0]
                    huxing = split_titleinfo[1]
                    area = split_titleinfo[2]
                else:
                    xiaoqu = split_titleinfo[0]
                    huxing = ""
                    area = ""
                # 朝向、装修
                houseInfo = infolist[0].find_all(attrs={'class': "houseInfo"})
                split_houseinfo = houseInfo[0].get_text().split(" | ")
                direction = split_houseinfo[0]
                zxtype = split_houseinfo[1]
                # 成交时间
                dealDateInfo = infolist[0].find_all(attrs={'class': "dealDate"})
                dealDate = dealDateInfo[0].string
                # 成交总价
                totalPriceInfo = infolist[0].find_all(attrs={'class': "totalPrice"})
                totalPrice = totalPriceInfo[0].find_all(attrs={'class': "number"})[0].string
                # 楼层、房屋建设时间
                positionInfo = infolist[0].find_all(attrs={'class': "positionInfo"})
                positionIcon = positionInfo[0].get_text().split(" ")
                floor = positionIcon[0]
                years = positionIcon[1]
                # 单价
                unitPriceInfo = infolist[0].find_all(attrs={'class': "unitPrice"})
                unitPrice = unitPriceInfo[0].find_all(attrs={'class': "number"})[0].string
                # 挂牌价格、成交周期
                dealCycleeInfo = infolist[0].find_all(attrs={'class': "dealCycleeInfo"})
                dealCycleTxt = dealCycleeInfo[0].find_all(attrs={'class': "dealCycleTxt"})
                dealCycleTxt_span = dealCycleTxt[0].find_all("span")
                if (len(dealCycleTxt_span) == 2):
                    listPrice = dealCycleTxt_span[0].get_text()
                    dealCycle = dealCycleTxt_span[1].get_text()
                elif (len(dealCycleTxt_span) == 1):
                    if ("成交周期" in dealCycleTxt_span[0].get_text()):
                        dealCycle = dealCycleTxt_span[0].get_text()
                        listPrice = ""
                    if ("挂牌" in dealCycleTxt_span[0].get_text()):
                        listPrice = dealCycleTxt_span[0].get_text()
                        dealCycle = ""

                houselist.append(
                    [address, xiaoqu, huxing, area, direction, zxtype, dealDate, totalPrice, floor, years, unitPrice, \
                     listPrice, dealCycle])

if __name__ == "__main__":
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                                   (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
    }
    # 浦东、杨浦、宝山
    addresslist = ["beicai", "biyun", "caolu", "chuansha", "datuanzhen", "gaodong", "gaohang", "geqing", "hangtou", \
                   "huamu", "huinan", "jinqiao", "jinyang", "kangqiao", "laogangzhen", "lianyang", "lingangxincheng", \
                   "lujiazui", "meiyuan1", "nanmatou", "nichengzhen", "sanlin", "shibo", "shuyuanzhen", "tangqiao", \
                   "tangzhen", "waigaoqiao", "wanxiangzhen", "weifang", "xinchang", "xuanqiao", "yangdong", "yangjing", \
                   "yangsiqiantan", "yuanshen", "yuqiao1", "zhangjiang", "zhoupu", "zhuqiao", "anshan", "dongwaitan", \
                   "huangxinggongyuan", "kongjianglu", "wujiaochang", "xinjiangwancheng", "zhongyuan1", "zhoujiazuilu", \
                   "dachangzhen", "dahua", "gaojing", "gongfu", "gongkang", "gucun", "luodian", "luojing", "shangda", \
                   "songbao", "songnan", "tonghe", "yanghang", "yuepu", "zhangmiao"]
    # 最终爬取的成交信息
    houselist = []
    # 总记录数
    cnt = 0

    spiderSecHouse(addresslist, headers, houselist, cnt)

    #保存为csv
    columns = ["address", "xiaoqu", "huxing", "area", "chaoxiang", "zxtype", "dealDate", "totalPrice", "floor", "years", \
               "unitPrice", "listPrice", "dealCycle"]

    df = pd.DataFrame(columns=columns, data=houselist)
    df.to_csv("secHand_add.csv", mode='a', encoding="gbk")

    #secHand.csv 不带区域信息
    #secHand_address.csv 带区域信息 挂牌价格 成交周期有误
    #secHand_add.csv 带区域信息 挂牌价格 成交周期无误