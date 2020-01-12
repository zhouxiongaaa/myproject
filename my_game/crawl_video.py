import requests
import re
import urllib

URL = 'http://www.pearvideo.com/video_1367621'


def load_video(url):
    hd = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    html = requests.get(url, headers=hd).text
    url_MP4 = re.compile(r'(http://video.*?mp4.*?mp4)', re.S)
    url_MP4s = re.findall(url_MP4, html)
    print(url_MP4s)
    # for i in url_MP4s:
    #     print(i)
    #     urllib.request.urlretrieve(i, 'haha.mp4')
    #     print('下载成功')


if __name__ == '__main__':
    load_video(URL)
