# -*- coding: utf-8 -*-
# 爬取智联招聘中的某个职位的职位数，并统计其平均工资。
import re
import json
import requests


def enter_page_and_get_json(i, j):
    global job_num, ave_salary
    ave_salary = 0
    url = 'https://fe-api.zhaopin.com/c/i/sou?start=0&pageSize=90&cityId='+i+'&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw='+j+'&kt=3'
    wbdata = requests.get(url).text  # 对HTTP响应的数据JSON化.
    data = json.loads(wbdata)
    # print(data)
    job_num = data['data']['count']
    n = int(int(job_num)/90)
    for x in range(n+1):
        y = x*90
        y = str(y)
        try:
            url = 'https://fe-api.zhaopin.com/c/i/sou?start='+y+'&pageSize=90&cityId='+i+'&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw='+j+'&kt=3'
            wbdata = requests.get(url).text  # 对HTTP响应的数据JSON化.
            data = json.loads(wbdata)
            for n in range(91):
                try:
                    string = data['data']['results'][n]['salary']
                    salary_list = re.findall(r"\d+\.?\d*", string)
                    ave = (float(salary_list[0]) + float(salary_list[1]))/2
                    ave_salary += ave
                except: continue
        except: continue
        # print(ave_salary)
    ave_salary = round(ave_salary*1000/int(job_num), 3)

    return job_num, ave_salary


if __name__ == '__main__':
    city_name = input('请输入你要查询的城市，并以空格分隔：')
    job_name = input('请输入你要查询的职位：')
    city_list = city_name.split(' ')
    for city in city_list:
        enter_page_and_get_json(city, job_name)
        print(''+city+'的岗位数为'+str(job_num)+'')
        print(''+city+'的平均薪资为'+str(ave_salary)+'')
