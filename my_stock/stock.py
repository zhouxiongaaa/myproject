# -*- coding: utf-8 -*-
'''获取中财网的基金重仓股，持股家数排序持，股家数大于5的，并持股家数增加的前几页股票，
并获取股票相关数据存入MySQL'''
import time
import mysql.connector
from selenium import webdriver


def enter_page_and_get_data(j):
    global s_name, s_code, s_price, industry, turnover_rate, pe_ratio, pb_ratio, net_yield, gross_profit_margin
    driver.get(j)
    s_name = driver.find_element_by_xpath('//*[@id="act_quote"]/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div[1]').text[:-8]
    s_code = driver.find_element_by_xpath('//*[@id="act_quote"]/table/tbody/tr/td[1]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div[1]').text[-7:-1]
    s_price = driver.find_element_by_xpath('//*[@id="last"]').text[:-1]
    industry = driver.find_element_by_xpath('//*[@id="act_quote"]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/a').text
    turnover_rate = driver.find_element_by_xpath('//*[@id="quotetab_stock"]/tbody/tr[1]/td[4]').text[4:]
    pe_ratio = driver.find_element_by_xpath('//*[@id="quotetab_stock"]/tbody/tr[3]/td[1]').text[4:]
    pb_ratio = driver.find_element_by_xpath('//*[@id="quotetab_stock"]/tbody/tr[4]/td[1]').text[4:]
    driver.find_element_by_xpath('//*[@id="nodea1"]/nobr/a').click()
    net_yield = driver.find_element_by_xpath('//*[@id="content"]/div[2]/table/tbody/tr[26]/td[2]/font').text
    gross_profit_margin = driver.find_element_by_xpath('//*[@id="content"]/div[2]/table/tbody/tr[39]/td[2]/font').text
    return s_name, s_code, s_price, industry, turnover_rate, pe_ratio, pb_ratio, net_yield, gross_profit_margin



def deposit():
    cur.execute("INSERT INTO stock_data"
                "(num, s_name, s_code, s_price, industry, turnover_rate, pe_ratio, pb_ratio, net_yield, gross_profit_margin)"
                "VALUES(null, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (s_name, s_code, s_price, industry, turnover_rate, pe_ratio, pb_ratio, net_yield, gross_profit_margin))


if __name__ == '__main__':
    conn = mysql.connector.connect(user='root', password='a4592948',
                                   host='localhost', port='3306',
                                   database='fund', use_unicode=True)
    cur = conn.cursor()

    driver = webdriver.Chrome(r'C:\Users\Zhouxiong\AppData\Local\Google\Chrome\Application\chromedriver.exe')  # 打开谷歌浏览器
    driver.get("http://data.cfi.cn/cfidata.aspx?ndk=A0A1934A1937A2196A4834")
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="myFrame"]/frame[3]'))
    stock_url_list = []
    page_num = 11
    while page_num <= 1:
        for i in range(2, 52):
            i = str(i)
            try:
                stock = driver.find_element_by_xpath('//*[@id="content"]/table[2]/tbody/tr['+i+']/td[3]/a')
                stock_url = stock.get_attribute("href")
                var = driver.find_element_by_xpath('//*[@id="content"]/table[2]/tbody/tr['+i+']/td[8]/font').text
                # print(stock_url, var, type(var))
                if int(var) > 0:
                    stock_url_list.append(stock_url)
            except:
                print(''+stock_url+'获取持股家数失败')
                continue
        driver.find_element_by_xpath('//*[@id="content"]/div[3]/a[77]').click()
        page_num += 1
        time.sleep(3)
        print(len(stock_url_list))
    for j in stock_url_list:
        try:
            enter_page_and_get_data(j)
            deposit()
        except:
            print(''+j+'获取失败')
            continue
    conn.commit()
    cur.close()
    conn.close()
    driver.quit()

