# prrs
publication retrieval and recommendate system

基于DBpedia的出版物检索和推荐系统

## 设计思路

根据需求描述，该系统主要包括三个功能：检索、推荐及展示，主要设计思路如下：

1. 检索部分：用户通过输入关键词，在书籍、电影、游戏三种出版物资源中查找名称匹配的资源，获取相应字段输出
2. 推荐部分：根据检索召回结果，继续查询与召回结果在关键属性上相同且名称不一致的资源。三种类型出版物的关键属性不尽相同，比如书籍部分的关键属性使用了作者和出版社，电影部分使用了导演和主演等。推荐部分通过设置题名不一致的条件，规避过于相似的推荐。
3. 展示部分：将检索或推荐结果输出为html网页，其中需要根据不同的出版物涉及不同的表格，同时需要处理一些缩略图和链接跳转。

## 功能描述

1. 通过用户输入的关键词，检索相关的出版物资源，检索结果以html网页的格式展示。
2. 通过用户输入的关键词，为用户推荐用户可能也感兴趣的出版物资源，推荐结果同样以html网页的格式展示。

## 使用说明

以检索关键词"warcraft"为例:

    git clone https://github.com/zhleiling/prrs.git
    cd prrs/src
    python main.py warcraft
    cd ../result
    
结果目录下retrieval.html为检索结果的html网页，recommend.html为推荐结果的html网页

检索结果样例：<https://zhleiling.github.io/prrs/result/retrieval.html>

推荐结果样例：<https://zhleiling.github.io/prrs/result/recommend.html>
