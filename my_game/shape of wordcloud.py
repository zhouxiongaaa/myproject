import jieba
import wordcloud
from PIL import Image
from scipy.misc import imread

start_pit_name = input('请输入你要处理成的形状的图片名x.jpg:')
wordfile_name = input('请输入你存储词云的文件名x.txt:')
save_pit_name = input('请输入你要保存的图片名x.jpg:')


def wordcloud_picture(i, j, s):
    mask = imread('C:\\Users\\Zhouxiong\\Desktop\\形状词云\\'+i+'')
    with open('C:\\Users\\Zhouxiong\\Desktop\\形状词云\\'+j+'') as f:
        ls = jieba.lcut(f.read())
    txt = ' '.join(ls)
    w = wordcloud.WordCloud(background_color='white', mask=mask, font_path='C:\\Windows\\Fonts\\Deng.ttf')  # 需要设置字体，不然会乱码
    w.generate(txt)
    w.to_file(''+s+'')


if __name__ == '__main__':
    wordcloud_picture(start_pit_name, wordfile_name, save_pit_name)
