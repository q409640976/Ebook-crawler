# 恩京の书房

## 使用说明

这个脚本是用于i-book.in的后端爬虫组件之一，其功能是自动更新恩京の书房内的图书。

### 流程

使用Algolia的数据对比 **恩京の书房** 更新数据，下载Algolia内没有的图书，并且上传到ipfs，将数据添加到Algolia，最后推送通知到指定设备。

### 需要的库

```bash
pip3 install algoliasearch
pip3 install ipfshttpclient
pip3 install fake_useragent
```
