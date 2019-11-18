# coding: utf-8
#!/usr/bin/python3
import os
import sys
import json
import urllib.request
import re
import urllib
import random,time
from algoliasearch.search_client import SearchClient
#from fake_useragent import UserAgent #随机UserAgent，可选。
#import ipfshttpclient #ipfs功能，可选。
#clients = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
client = SearchClient.create('Application ID', 'Admin API Key')#Algolia的key。
index = client.init_index('book')
booklist = 0 
def crawl (str):
    ua = UserAgent()
    #headers = json.loads('{"User-Agent": "'+ua.random+'"}')#随机UserAgent 可选
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    req = urllib.request.Request(url=str, headers=headers)
    res = urllib.request.urlopen(req)
    html = res.read().decode('utf-8')
    html=html.replace("\n", "")
    html=html.replace("\t", "")
    html=html.replace("\r", "")
    return html
for pages in range(1,3):
    print('正在解析第%s页'%pages)
    rawpage = crawl(str = 'https://www.enjing.com/page/%s/' %pages)
    if '404' in rawpage:
        print('第%s页，出现错误。'%pages)
        break
    else:
        bookurls = re.findall(r'rel="bookmark" href="(.+?).htm">',rawpage)
        booknames = re.findall(r'<a target="_blank" title="(.+?)" rel="bookmark"',rawpage)#书名
        for (bookname,bookurl) in zip(booknames,bookurls):
            print('正在解析：《%s》'%bookname,end='')
            algoliaraw = str(index.search(bookname))
            DBnames = re.findall(r"name': '(.*?)', '",algoliaraw)
            if bookname in DBnames:
                print('\033[0;32;40m已存在!\033[0m')
            else:
                infopage = crawl(str = '%s.htm' %bookurl)
                try:
                    author = re.findall(r'<p>作者：(.+?)</p>',infopage)#作者
                except:
                    author = 'none'
                intor = re.findall(r'</table> --><p>(.+?)</p>', infopage)#简介
                dlinks = re.findall(r'download.php(.+?)"  targe', infopage)#下载页面
                imgs = re.findall(r'shudan.io(.+?)"', infopage)#img
                getimgurl = imgs[0]
                imgname = getimgurl.replace("/", "")
                getimg = '/usr/bin/wget -x -q --user-agent="Mozilla/5.0" -O ./img/'+imgname+' https://shudan.io/'+getimgurl
                os.system(getimg)#下载图片
                jsons = '{"name": "'+bookname+'","Author": "'+author[0]+'","intor": "'+intor[0]+'","link": "'+bookname+'","img": "'+imgname+'"},'
                fileObject = open('ejraw.json', 'a')#将获取到的原始json保存（归档）
                fileObject.write(jsons)
                fileObject.write('\n')
                fileObject.close()
                dlinks = re.findall(r'download.php(.+?)"  targe', infopage)#下载页面
                dlinks = 'https://www.enjing.com/download.php'+dlinks[0]
                rawlink = crawl(str = r'%s' % dlinks)#解析下载页面
                rawlink = re.findall(r'格式：</span><span><a href="(.+?).epub" target=', rawlink)
                rawlink = rawlink[0]
                bookfolder=str('mkdir ./book/'+bookname)
                os.system(bookfolder)
                ebooktypes=['.epub ','.mobi ','.azw3 ']
                for ebooktype in ebooktypes:
                    downlinks=str('/usr/bin/wget -x -t 3 -T 10 -nv -q --user-agent="Mozilla/5.0" -O ./book/'+bookname+'/'+bookname+ebooktype+rawlink+ebooktype)
                    os.system(downlinks)
                #ipfs功能，可选。
                '''
                upbk = r'./book/%s' % bookname
                upim = r'./img/%s' % imgname
                ipfsbook = clients.add(upbk)#上传到ipfs，并解析hash到json
                ipfsimg = clients.add(upim)
                ipfsbook=str(ipfsbook)
                ipfsimg=str(ipfsimg)
                ipfsbook  = re.findall(r"Qm(.+?)'",ipfsbook)
                ipfsbook= ipfsbook[-1]
                ipfsimg  = re.findall(r"Qm(.+?)'",ipfsimg)
                ipfsimg = ipfsimg[0]
                ipfsjsons = '{"name": "'+bookname+'","Author": "'+author[0]+'","intor": "'+intor[0]+'","link": "https://1.i-book.in/ipfs/Qm'+ipfsbook+'","img": "https://1.i-book.in/ipfs/Qm'+ipfsimg+'"},'
                res = index.save_objects([{'name': ''+bookname+'','Author': ''+author[0]+'','intor': ''+intor[0]+'','link': 'https://1.i-book.in/ipfs/Qm'+ipfsbook+'','img': 'https://1.i-book.in/ipfs/Qm'+ipfsimg+''},], {'autoGenerateObjectIDIfNotExist': True})
                fileObject = open('ejipfs.josn', 'a')#将获取到的ipfs格式的json保存                                  
                for post in ipfsjsons:
	                fileObject.write(post)
                fileObject.close()
                '''
                print("\033[0;32;40m done\033[0m")
                booklist=booklist+1 #成功下载的图书计数
os.system("curl -s 'https://api.day.app/Bark-API/恩京的书房更新了 "+str(booklist)+" 本书。?url=https://i-book.in' > /dev/null")
