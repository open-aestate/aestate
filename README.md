<p align="center">
<img width="40%" src="https://summer-publiced.oss-cn-hangzhou.aliyuncs.com/logos/logo_framework_tr.png"/>
</p>
<h1 align="center">Aestate —— 多样化数据库查询</h1>
<p align="center">
  <img src="https://img.shields.io/badge/python-%3E%3D%203.6-blue.svg" />
  <a href="http://doc.cacode.ren">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" target="_blank" />
  </a>
  <a href="https://gitee.com/cacode_cctvadmin/summer-python/blob/main/LICENSE">
    <img alt="License: Apache-2.0" src="https://img.shields.io/badge/License-Apache--2.0-yellow.svg" target="_blank" />
  </a>
</p>

# 介绍

> 当前仅MySql测试通过

`Aestate Framework` 是一款基于`Python`语言开发的`ORM`框架，你可以使用多种方式去实现基于对象方式的查询.

比如使用类似`django`的模式去使用：modelClass.opera.filter(*args, **kwargs)

或者sqlalchemy的方式：find(*args).find_from(table).where(**kwargs).group_by(*args)

或者像`java`的`hibernate`一样：

```python
def findAllWhereIdAndName(id, name) -> list: ...
```

或者像`java`的`mybatis`使用xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<body>
    <database id="demo" user="root" password="12345"/>
    <database id="demo_2" user="root" password="12345"/>
    <item anme="" db="demo">
        <select name="表名">
            <if id="{$id>0}">
                <!--符号是：[==:等于,!=:不等于,>>:大于,<<小于,>=:大于等于,<=:小于等于,^^:like,!^:not like]-->
                <where name="==$name" id=">>$id"/>
            </if>
            <elif>
                <where id=">>$id+10"/>
            </elif>
            <else>
                <where id=">>$id+100"/>
            </else>
        </select>
    </item>
</body>
```

# 先决条件

> python >=3.6 (其他版本没试过)  
> 教程文档地址：http://doc.cacode.ren

# 更全面的教程和文档

- [文字教程 doc.cacode.ren](http://doc.cacode.ren)
- [视频教程 bilibili.com](https://www.bilibili.com/video/BV1gq4y1E7Fs/)

# 安装

> pip 命令：pip install aestate  
> anaconda 安装：conda install aestate  
> qq群：[909044439](https://jq.qq.com/?_wv=1027&k=EK7YEXmh)

# 依赖包

> pip install aestate-json

# 谁在使用 Aestate Framework 开发网站

CACode： [https://cacode.ren](https://cacode.ren)  
CocoZao 爬虫：[https://ccz.cacode.ren](https://ccz.cacode.ren)
> 开源示例项目：[gitee/aestate-example](https://gitee.com/canotf/aestate-example)

# CACode Development Team

> Last edit time:2021/05/26 02:03 Asia/Shanghai   
> [👉 Go to canotf`s homepage on Gitee 👈](https://gitee.com/canotf)
