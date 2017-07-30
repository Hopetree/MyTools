import requests
from bs4 import BeautifulSoup as bs
import re
import time
import datetime

class myLIST():
    def __init__(self):
        self.musicstyle = {'民谣': 'http://music.163.com/discover/playlist/?cat=%E6%B0%91%E8%B0%A3',
                       '感动': 'http://music.163.com/discover/playlist/?cat=%E6%84%9F%E5%8A%A8',
                       '伤感': 'http://music.163.com/discover/playlist/?cat=%E4%BC%A4%E6%84%9F',
                       '钢琴': 'http://music.163.com/discover/playlist/?cat=%E9%92%A2%E7%90%B4',
                       '影视原声': 'http://music.163.com/discover/playlist/?cat=%E5%BD%B1%E8%A7%86%E5%8E%9F%E5%A3%B0',
                       '翻唱': 'http://music.163.com/discover/playlist/?cat=%E7%BF%BB%E5%94%B1',
                       '说唱': 'http://music.163.com/discover/playlist/?cat=%E8%AF%B4%E5%94%B1',
                       '治愈': 'http://music.163.com/discover/playlist/?cat=%E6%B2%BB%E6%84%88',
                       '朋克': 'http://music.163.com/discover/playlist/?cat=%E6%9C%8B%E5%85%8B',
                       '雷鬼': 'http://music.163.com/discover/playlist/?cat=%E9%9B%B7%E9%AC%BC',
                       '器乐': 'http://music.163.com/discover/playlist/?cat=%E5%99%A8%E4%B9%90',
                       '校园': 'http://music.163.com/discover/playlist/?cat=%E6%A0%A1%E5%9B%AD',
                       '工作': 'http://music.163.com/discover/playlist/?cat=%E5%B7%A5%E4%BD%9C',
                       '游戏': 'http://music.163.com/discover/playlist/?cat=%E6%B8%B8%E6%88%8F',
                       'ACG': 'http://music.163.com/discover/playlist/?cat=ACG',
                       '日语': 'http://music.163.com/discover/playlist/?cat=%E6%97%A5%E8%AF%AD',
                       '欧美': 'http://music.163.com/discover/playlist/?cat=%E6%AC%A7%E7%BE%8E',
                       '散步': 'http://music.163.com/discover/playlist/?cat=%E6%95%A3%E6%AD%A5',
                       '吉他': 'http://music.163.com/discover/playlist/?cat=%E5%90%89%E4%BB%96',
                       '舞曲': 'http://music.163.com/discover/playlist/?cat=%E8%88%9E%E6%9B%B2',
                       '另类/独立': 'http://music.163.com/discover/playlist/?cat=%E5%8F%A6%E7%B1%BB%2F%E7%8B%AC%E7%AB%8B',
                       '粤语': 'http://music.163.com/discover/playlist/?cat=%E7%B2%A4%E8%AF%AD',
                       '兴奋': 'http://music.163.com/discover/playlist/?cat=%E5%85%B4%E5%A5%8B',
                       '爵士': 'http://music.163.com/discover/playlist/?cat=%E7%88%B5%E5%A3%AB',
                       '经典': 'http://music.163.com/discover/playlist/?cat=%E7%BB%8F%E5%85%B8',
                       '旅行': 'http://music.163.com/discover/playlist/?cat=%E6%97%85%E8%A1%8C',
                       '70后': 'http://music.163.com/discover/playlist/?cat=70%E5%90%8E',
                       'New Age': 'http://music.163.com/discover/playlist/?cat=New%20Age',
                       '摇滚': 'http://music.163.com/discover/playlist/?cat=%E6%91%87%E6%BB%9A',
                       '华语': 'http://music.163.com/discover/playlist/?cat=%E5%8D%8E%E8%AF%AD',
                       '小语种': 'http://music.163.com/discover/playlist/?cat=%E5%B0%8F%E8%AF%AD%E7%A7%8D',
                       '思念': 'http://music.163.com/discover/playlist/?cat=%E6%80%9D%E5%BF%B5',
                       '浪漫': 'http://music.163.com/discover/playlist/?cat=%E6%B5%AA%E6%BC%AB',
                       '古风': 'http://music.163.com/discover/playlist/?cat=%E5%8F%A4%E9%A3%8E',
                       '电子': 'http://music.163.com/discover/playlist/?cat=%E7%94%B5%E5%AD%90',
                       '榜单': 'http://music.163.com/discover/playlist/?cat=%E6%A6%9C%E5%8D%95',
                       '快乐': 'http://music.163.com/discover/playlist/?cat=%E5%BF%AB%E4%B9%90',
                       '英伦': 'http://music.163.com/discover/playlist/?cat=%E8%8B%B1%E4%BC%A6',
                       '清晨': 'http://music.163.com/discover/playlist/?cat=%E6%B8%85%E6%99%A8',
                       'R&B/Soul': 'http://music.163.com/discover/playlist/?cat=R%26B%2FSoul',
                       '性感': 'http://music.163.com/discover/playlist/?cat=%E6%80%A7%E6%84%9F',
                       '乡村': 'http://music.163.com/discover/playlist/?cat=%E4%B9%A1%E6%9D%91',
                       '儿童': 'http://music.163.com/discover/playlist/?cat=%E5%84%BF%E7%AB%A5',
                       '网络歌曲': 'http://music.163.com/discover/playlist/?cat=%E7%BD%91%E7%BB%9C%E6%AD%8C%E6%9B%B2',
                       '古典': 'http://music.163.com/discover/playlist/?cat=%E5%8F%A4%E5%85%B8',
                       '驾车': 'http://music.163.com/discover/playlist/?cat=%E9%A9%BE%E8%BD%A6',
                       '韩语': 'http://music.163.com/discover/playlist/?cat=%E9%9F%A9%E8%AF%AD',
                       'Bossa Nova': 'http://music.163.com/discover/playlist/?cat=Bossa%20Nova',
                       '夜晚': 'http://music.163.com/discover/playlist/?cat=%E5%A4%9C%E6%99%9A',
                       '80后': 'http://music.163.com/discover/playlist/?cat=80%E5%90%8E',
                       '流行': 'http://music.163.com/discover/playlist/?cat=%E6%B5%81%E8%A1%8C',
                       'KTV': 'http://music.163.com/discover/playlist/?cat=KTV',
                       '下午茶': 'http://music.163.com/discover/playlist/?cat=%E4%B8%8B%E5%8D%88%E8%8C%B6',
                       '拉丁': 'http://music.163.com/discover/playlist/?cat=%E6%8B%89%E4%B8%81',
                       '怀旧': 'http://music.163.com/discover/playlist/?cat=%E6%80%80%E6%97%A7',
                       '90后': 'http://music.163.com/discover/playlist/?cat=90%E5%90%8E',
                       '清新': 'http://music.163.com/discover/playlist/?cat=%E6%B8%85%E6%96%B0',
                       '酒吧': 'http://music.163.com/discover/playlist/?cat=%E9%85%92%E5%90%A7',
                       '地铁': 'http://music.163.com/discover/playlist/?cat=%E5%9C%B0%E9%93%81',
                       '安静': 'http://music.163.com/discover/playlist/?cat=%E5%AE%89%E9%9D%99',
                       '午休': 'http://music.163.com/discover/playlist/?cat=%E5%8D%88%E4%BC%91',
                       '民族': 'http://music.163.com/discover/playlist/?cat=%E6%B0%91%E6%97%8F',
                       '孤独': 'http://music.163.com/discover/playlist/?cat=%E5%AD%A4%E7%8B%AC',
                       '轻音乐': 'http://music.163.com/discover/playlist/?cat=%E8%BD%BB%E9%9F%B3%E4%B9%90',
                       '世界音乐': 'http://music.163.com/discover/playlist/?cat=%E4%B8%96%E7%95%8C%E9%9F%B3%E4%B9%90',
                       '后摇': 'http://music.163.com/discover/playlist/?cat=%E5%90%8E%E6%91%87',
                       '00后': 'http://music.163.com/discover/playlist/?cat=00%E5%90%8E',
                       '金属': 'http://music.163.com/discover/playlist/?cat=%E9%87%91%E5%B1%9E',
                       '学习': 'http://music.163.com/discover/playlist/?cat=%E5%AD%A6%E4%B9%A0',
                       '运动': 'http://music.163.com/discover/playlist/?cat=%E8%BF%90%E5%8A%A8',
                       '蓝调': 'http://music.163.com/discover/playlist/?cat=%E8%93%9D%E8%B0%83',
                       '放松': 'http://music.163.com/discover/playlist/?cat=%E6%94%BE%E6%9D%BE'}

class myAPI():
    def __init__(self):
        self.headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWeb'
                                     'Kit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        self.file_time = datetime.datetime.strftime(datetime.datetime.now(),"%Y%m%d%H%M")  #时间

    # 按照当前时间创建一个表格文件，文件名称是时间加上风格
    def get_csv(self,music_style):
        filename = "{}_{}.csv".format(self.file_time,music_style)
        titles = ['歌曲id','歌名','歌手id','歌手','专辑id','专辑名','歌曲链接']
        with open(filename,"w") as f:
            f.write(",".join(titles)+"\n")
        return filename

    # 获取一个风格的所有歌单链接
    def get_song_list(self,style_link,pagenum):
        song_list = []
        for x in range(0,int(pagenum)):
            the_url = style_link+'&limit=35&offset={}'.format(x*35)
            res = requests.get(the_url,headers=self.headers)
            html = res.text
            soup = bs(html,'lxml')
            play_lists = soup.select('.m-cvrlst > li')
            for play_list in play_lists:
                title = play_list.select('.dec > a')[0].get('title')
                play_link = 'http://music.163.com'+play_list.select('.dec > a')[0].get('href')
                song_list.append(play_link)
        return song_list

    # 获取单个歌单的歌曲信息
    def get_onestyle(self,onelink,filename):
        # 声明这两个变量的目的是为了后面使用eval函数不报错
        null = ''
        false = ''
        true = ''
        html = requests.get(onelink, headers=self.headers).text
        soup = bs(html, 'lxml')
        try:
            data = soup.find_all('textarea', {'style': 'display:none;'})[0].text.strip()
            song_list = eval(data)
            for song in song_list:
                song_id = str(song['id'])
                song_name = song['name'].strip().replace(',', '，').replace(' ', '')
                # 由于歌手可能不止一个，所以是一个列表，因此可以把歌手名字和ID组合起来
                singers = song['artists']
                singer_names = []
                singer_ids = []
                for info in singers:
                    singer_names.append(info['name'].strip().replace(',', '，').replace(' ', ''))
                    singer_ids.append(str(info['id']))
                singer_name = '&'.join(singer_names) if len(singers) > 1 else info['name'].strip().replace(',',
                                                                                                           '，').replace(
                    ' ', '')
                singer_id = '&'.join(singer_ids) if len(singers) > 1 else str(info['id'])

                album_id = str(song['album']['id'])
                album = song['album']['name'].strip().replace(',', '，').replace(' ', '')
                song_link = 'http://music.163.com/song?id=' + str(song_id)
                try:
                    with open(filename, 'a') as f:
                        this_list = [song_id, song_name, singer_id, singer_name, album_id, album, song_link]
                        f.write(','.join(this_list) + '\n')
                except UnicodeEncodeError:
                    with open(filename, 'a') as f:
                        this_list = [song_id, song_name, singer_id, singer_name, album_id, album, song_link]
                        f.write(','.join(this_list).encode("gbk", "ignore").decode("gbk") + '\n')
                except Exception as e:
                    pass
        # 有的信息不规范，不能将字符串转换成列表，因此使用try语句
        except SyntaxError:
            the_list = soup.select('.f-hide > li > a')
            for song in the_list:
                song_name = song.text.strip().replace(' ', '').replace(',', '，')
                song_id = re.findall('id=(.*)', song.get('href').strip().replace(' ', '').replace(',', '，'))[0]
                song_link = 'http://music.163.com/song?id=' + song_id
                singer_id = ''
                singer_name = ''
                album_id = ''
                album = ''
                try:
                    with open(filename, 'a') as f:
                        this_list = [song_id, song_name, singer_id, singer_name, album_id, album, song_link]
                        f.write(','.join(this_list) + '\n')
                except UnicodeEncodeError:
                    with open(filename, 'a') as f:
                        this_list = [song_id, song_name, singer_id, singer_name, album_id, album, song_link]
                        f.write(','.join(this_list).encode("gbk", "ignore").decode("gbk") + '\n')
                except Exception as e:
                    pass
        except Exception as e:
            pass

if __name__ == '__main__':
    myapi = myAPI()
    file = myapi.get_csv("华语")
    print(file)

