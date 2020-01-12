# import you-get
# 爬取bilibili上李子柒的视频
import os
import json
import requests

for i in range(1, 5):
    i = str(i)
    url = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=19577966&pagesize=30&tid=0&page='+i+''
    wbdata = requests.get(url).text
    # 对HTTP响应的数据JSON化.
    data = json.loads(wbdata)

    for j in range(31):
        try:
            num = data['data']['vlist'][j]['aid']
            video_url = 'https://www.bilibili.com/video/av' + str(num)
            print(j, video_url, type(video_url))
        #   os.system('you-get video_url')
        except:
            print('第'+i+'页video_url已获取完了')
            break


