# -*- coding: utf-8 -*-
'''获取中财网的ST股票，并获取股票相关数据存入MySQL'''
import time
import mysql.connector
from selenium import webdriver


def enter_page_and_get_data(j):
    global stock_name, s_price, industry, turn, shiyin, shijing, jinshouyilv, xiaoshoumaolvlv, meiguyinye
    driver.get(j)
    stock_name = driver.find_element_by_xpath('//*[@id="act_quote"]/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div[1]').text
    s_price = driver.find_element_by_xpath('//*[@id="last"]').text[:-1]
    industry = driver.find_element_by_xpath('//*[@id="act_quote"]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/a').text
    turn = driver.find_element_by_xpath('//*[@id="quotetab_stock"]/tbody/tr[1]/td[4]').text[4:]
    shiyin = driver.find_element_by_xpath('//*[@id="quotetab_stock"]/tbody/tr[3]/td[1]').text[4:]
    shijing = driver.find_element_by_xpath('//*[@id="quotetab_stock"]/tbody/tr[4]/td[1]').text[4:]
    driver.find_element_by_xpath('//*[@id="nodea1"]/nobr/a').click()
    jinshouyilv = driver.find_element_by_xpath('//*[@id="content"]/div[2]/table/tbody/tr[26]/td[2]/font').text
    xiaoshoumaolvlv = driver.find_element_by_xpath('//*[@id="content"]/div[2]/table/tbody/tr[39]/td[2]/font').text
    meiguyinye = driver.find_element_by_xpath('//*[@id="content"]/div[2]/table/tbody/tr[10]/td[2]/font').text[:-3]
    return stock_name, s_price, industry, turn, shiyin, shijing, jinshouyilv, xiaoshoumaolvlv, meiguyinye



def deposit():
    cur.execute("INSERT INTO st_data"
                "(num, s_name, s_price, industry, turn, shiyin, shijing, jinshouyilv, xiaoshoumaolvlv, shixiaolv)"
                "VALUES(null, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (stock_name, s_price, industry, turn, shiyin, shijing, jinshouyilv, xiaoshoumaolvlv, shixiaolv))


if __name__ == '__main__':
    conn = mysql.connector.connect(user='root', password='a4592948',
                                   host='localhost', port='3306',
                                   database='fund', use_unicode=True)
    cur = conn.cursor()

    driver = webdriver.Chrome(r'C:\Users\Zhouxiong\AppData\Local\Google\Chrome\Application\chromedriver.exe')  # 打开谷歌浏览器
    driver.get("http://data.cfi.cn/cfidata.aspx?ndk=A0A1934A1937A2196A4834")
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="myFrame"]/frame[3]'))
    stock_url_list = []
    page_num = 1
    while page_num <= 77:
        for i in range(2, 52):
            i = str(i)
            try:
                stock = driver.find_element_by_xpath('//*[@id="content"]/table[2]/tbody/tr['+i+']/td[3]/a')
                stock_url = stock.get_attribute("href")
                var = driver.find_element_by_xpath('//*[@id="content"]/table[2]/tbody/tr['+i+']/td[3]/a').text
                # print(stock_url, var, type(var))
                if 'ST' in var:
                    stock_url_list.append(stock_url)
            except:
                # print(''+stock_url+'获取失败')
                continue
        print(len(stock_url_list))
        if page_num == 77:
            break
        else:

            driver.find_element_by_xpath('//*[@id="content"]/div[3]/a['+str(page_num)+']').click()
            page_num += 1
            time.sleep(3)

    for j in stock_url_list:
        try:
            enter_page_and_get_data(j)
            shixiaolv = round(float(s_price)/float(meiguyinye), 3)
            deposit()
        except:
            print(''+j+'获取失败')
            continue
    conn.commit()
    cur.close()
    conn.close()
    driver.quit()

