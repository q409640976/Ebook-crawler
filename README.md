# Ebook-crawler

这里储存着一些工作在i-book.in的后端爬虫们。

使用了一些自动化流程，为i-book.in自动爬取并索引数据。

主站：[**i-book.in**](https://i-book.in)

备用站点：[**i-book.in for Algolia**](https://www.algolia.com/realtime-search-demo/i-book-in)

目前适配了**恩京の书房**。

-----

## 功能：

抓取最近更新的图书；

将获取到的图书文件以及封面上传到IPFS；

获取电子书的info并生成json文件；

上传到Algolia；

-----

## 使用方法

恩京の书房：enjing

-----

## 待修复

- 中文乱码问题，在Linux界面能够正常显示中文，但在Windows下使用WINSCP连接到Linux查看文件就不能正常显示，反之亦然。debug好多次，但是上传到IPFS显示正常，并且生成的json也正常，所以就先放一放了。



