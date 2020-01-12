# -*- coding: utf-8 -*-
# 按指定的基金行业爬取基金的十大持股，并存入MySQL。
import time
import json
import requests
import mysql.connector
from lxml import etree
from selenium import webdriver


def get_fund_name(j):
    global fund_name, url
    url_name = driver.find_element_by_xpath('//*[@id="ctl00_cphMain_gridResult"]/tbody/tr['+j+']/td[3]/a')
    url = url_name.get_attribute("href")
    response = requests.request('get', url)
    fund_xpath = etree.HTML(response.text)
    fund_name = fund_xpath.xpath('//*[@id="qt_fund"]/span[1]/text()')[0][7:]
    return fund_name, url

def get_share_json(url):
    global datas
    url1 = 'http://cn.morningstar.com/handler/quicktake.ashx?command=portfolio&fcid=' + url[-10:]
    wbdata = requests.get(url1).text  # 对HTTP响应的数据JSON化.
    data = json.loads(wbdata)
    # print(data)
    datas = data['Top10StockHoldings']
    return datas


def deposit(datas1):
    share_name = datas1[n]['HoldingName']
    cur.execute("INSERT INTO fund_type_share_data"
                "(id, share_name)"
                "VALUES(null, %s)",
                (str(share_name),))


if __name__ == '__main__':
    fund_type = input('请输入基金类型：消费，医，混合，计算机，指数/ETF，农业，信息，银行/保险/金融，物流，地产，新，所有股票基金：')
    conn = mysql.connector.connect(user='root', password='a4592948',
                                   host='localhost', port='3306',
                                   database='fund', use_unicode=True)
    cur = conn.cursor()
    driver = webdriver.Chrome(r'C:\Users\Zhouxiong\AppData\Local\Google\Chrome\Application\chromedriver.exe')  # 打开谷歌浏览器
    driver.get("http://cn.morningstar.com/fundselect/default.aspx")
    driver.find_element_by_id("ctl00_cphMain_cblCategory_0").click()
    driver.find_element_by_id("ctl00_cphMain_cblCategory_1").click()
    driver.find_element_by_id("ctl00_cphMain_cblCategory_2").click()
    driver.find_element_by_id("ctl00_cphMain_cblCategory_5").click()
    driver.find_element_by_id("ctl00_cphMain_btnGo").click()
    # print(driver.page_source)
    page_num = num = 1
    while page_num <= 8:  #有5页五星的。
        for i in range(2, 27):
            i = str(i)
            try:
                fund_data = get_fund_name(i)
                if fund_type in fund_data[0]:
                    print(num, fund_data, type(fund_data[0]))
                    get_share_json(fund_data[1])
                    for n in range(10):
                        deposit(datas)
                    num += 1
                elif fund_type == '所有股票基金':
                    print(num, fund_data[0])
                    get_share_json(fund_data[1])
                    for n in range(10):
                        try:
                            deposit(datas)
                        except:
                            print(fund_data[0]+'没有十大持股')
                            continue
                    num += 1
                else:
                    continue
            except KeyError:
                continue
        driver.find_element_by_link_text(">").click()
        page_num += 1
        time.sleep(3)
    conn.commit()
    cur.close()
    conn.close()
    driver.quit()
