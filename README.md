# Simple-Course-Streaming-Downloader


A simple python script dedicated to downloading encrypted HLS (HTTP live streaming). Developed to extract segment links from given m3u8 url and download .ts files simultaneously, though currently it cannot handle nested m3u8. Multi-thread download enabled in main.py based on concurrent.futures. The script saves .ts files in /tmp folder located in the same directory as main.py. After the download thread pool is emptied, the /tmp folder will be  deleted and the downloaded mp4 media file will generate in the same directory.

This repo is still updating to support more file types and cooool features such as website scraping, or auto-synchronizing a local copy of your online course playbacks, anytime the program is running and connectivity is available.

*教学网已经开放mp4下载直链，本repo提供的方法已经没有使用的必要！

教学网下载录播视频，21年暑假教学网录播视频更新为HLS格式+AES-128加密，本repo提供一个较为简陋的下载方法，需要自己用chrome开发者工具获取cookie和m3u8链接（好在贵校教学网的m3u8没有加nest）
其中main.py已更换为多线程下载，单线程下载的版本也予以保留，如果多线程出现漏包、顺序错误问题，则可采用Single-thread.py

开学大二，python代码水平不高，所以项目以精简为主，写这个最开始只是为了自己应急用，再者因为水平菜+时间仓促，所以没有做m3u8的自动爬取，国庆如果有时间就做GUI，并借助selenium实现cookie和资源的自动爬取，以降低使用门槛

如果有大佬懂python爬虫和抓包，则跪求一个更好的，带递归爬取、直链嗅探的更完善的版本

总共只需要修改代码的两处变量，注释里有详细的description
#北京大学教学网（为方便搜索orz）

FAQ：
  Q1.下载完成后视频文件在哪？

​    A1.与main.py在同一目录下

  Q2.怎么安装依赖（requirements.txt）

​    A2.命令行cd至main.py的目录，输入pip install -r requirements.txt

  Q3.安装pycryptodome出现报错

​    A3.参照https://jingyan.baidu.com/article/95c9d20d7784ebec4f75616e.html
