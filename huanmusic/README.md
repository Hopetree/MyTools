## 幻音歌单爬虫
### 目标网站 http://www.huanmusic.com/playlists
- 项目运行
</br>运行huanspider.py，按照需要的歌单时间修改链接中日期即可开始爬虫
- 项目结构
    - huanmusic.py
    </br>主爬虫文件，提取并保存信息
    - config.py
    </br>用来生成自定义headers的
    - savedata.py
    </br>构造信息的保存方式，信息保存到Excel中
- Spider思路
</br>1、请求http://net.huanmusic.com/g_v1_20170718这个链接，链接尾端显示了歌单日期，请求可以获取所有歌单信息
</br>2、从返回的JSON信息中提取歌单信息，并得到每个歌单的链接构成部分
</br>3、单独请求每个歌单链接获取更多歌单信息并形成最终JSON信息集
</br>4、将歌单信息写入Excel表格
- PS:这个二次元音乐网收集的歌单，其实挺好听的！


