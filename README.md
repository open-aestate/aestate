<p align="center">
<img width="40%" src="https://gitee.com/aecode/aestate/raw/dev/resource/logo.png"/>
</p>
<h1 align="center">Aestate —— 多样化数据库查询</h1>
<p align="center">
  <a href='https://gitee.com/aecode/aestate/stargazers'>
    <img src='https://svg.hamm.cn/gitee.svg?user=aecode&project=aestate&type=star' alt='star'/>
  </a>
<img src='https://svg.hamm.cn/gitee.svg?user=aecode&project=aestate&type=language' alt='star'/>
<img src='https://svg.hamm.cn/badge.svg?key=Python&value=>=3.6'/>

  <a href="https://doc.cacode.ren">
    <img src='https://svg.hamm.cn/badge.svg?key=Documentation&value=yes'/>
  </a>
  <a href="https://gitee.com/aecode/summer-python/blob/main/LICENSE">
    <img src='https://svg.hamm.cn/gitee.svg?user=aecode&project=aestate&type=license' alt='star'/>
  </a>
</p>

# 介绍

> 当前测试通过数据库有:

- MySql8.0
- Sqlserver2019
- PostgreSQL 13.3

`Aestate Framework` 是一款基于`Python`语言开发的`ORM`框架， 你可以使用多种方式去实现基于对象方式的查询.

也就是相对于Java语言的Mybatis-Plus

比如使用类似`Django`的模式去使用：```modelClass.orm.filter(*args, **kwargs)```

或者SQLAlchemy的方式：```find().where(**kwargs).group_by(*args)```

或者像`Java`的`Hibernate`一样：

```Python
@SelectAbst()
def find_all_F_where_id_in_and_name_like_order_by_id(self, **kwargs) -> list: ...


@Select("SELECT * FROM demo WHERE id=#{id} AND name=#{name}")
def find_all_where_id(self, id, name): ...
```

或者像`Java`的`Mybatis`使用xml

```xml
<?xml version="1.0"?>
<aestate xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="aestate  https://gitee.com/aecode/aestate-xml/blob/main/v1/tags.xsd"
         xmlns="aestate">
    <template id="templateField">
        id,name,password,create_time,update_time
        <description>测试模板</description>
    </template>
    <resultMap id="resultMapLeftJoin" type="example.table.demoModels.Demo">
        <result field="d1_id" properties="id"/>
        <result field="d1_name" properties="name"/>
        <result field="d1_password" properties="password"/>
        <foreign type="example.table.demoModels.Demo" name="demoJoin">
            <result field="d2_id" properties="id"/>
            <result field="d2_name" properties="name"/>
            <result field="d2_password" properties="password"/>
        </foreign>
    </resultMap>
    <item id="findAllById">
        <select resultType="resultMapLeftJoin">
            SELECT
            <!-- 导入查询的字段 -->
            <!--            <include from="templateField"/>-->
            <include from="tempSymbol"/>
            FROM demo as d1 LEFT JOIN demo as d2 ON d2.id = d1.id WHERE d1.id >
            <switch field="id">
                <case value="10">10</case>
                <case value="5">5</case>
                <default>#{id}</default>
            </switch>
            <if test="#{id}&gt;=20">AND d2.id > 20</if>
            <else>AND d2.id > 10</else>
            LIMIT 2

            <description>
                SELECT d1.`name` as d1_name,d1.`password` as d1_password,d1.`id` as d1_id, d2.`name` as
                d2_name,d2.`password` as d2_password,d2.`id` as d2_id FROM demo as d1 LEFT JOIN demo as d2 ON d2.id =
                d1.id WHERE d1.id > %s AND d2.id > 10 LIMIT 2
            </description>
        </select>
    </item>
</aestate>
```

# 相对于其他库有什么区别？

- 首先**Aestate**是基于Django、SQLAlchemy、Mybatis、Mybatis-Plus、SpringJPA整合起来的一个数据库支持库，
  融合了这么多第三方库首先一点就是他的操作方式是多种多样的。目前已有六种操作方法， 也就是Django模式、SQLAlchemy模式、xml模式、Mybatis-Plus模式，注解模式，原生模式。

- 其次就是在兼容性方面，由于这个世界上的数据库种类太多了没办法做到统一， **Aestate**保留了对其他小众数据库的实现接口，尽可能多兼容数据库。

- 数据库表方面，Django是会生成数据django自己系统内部的表，在迁移的时候呢如果做错一步可能对于新手 来讲后面的修复操作是极其难的，也未必能够在短时间内定位问题并修复。**Aestate**为了解决这个问题，将make
  和手动建表尽可能的兼容，不会生成额外的表和数据，也不会捆绑某个特定系统，将pojo/model复制出来可以直接为下一个项目使用。

- 缓存方面参考了Mybatis的实现方法并略微修改，**Aestate**有两个内存管理模块，用于保证数据的完整性， 当一些特别大的数据占满缓存时，**Aestate**
  会尽量多的去分配内存保证数据完整性，除外才会去管理内存（不建议操作大于系统内存2/10的数据）。**Aestate**有弹性内存管理方式，会根据系统的执行自动调整缓存大小，尽可能的加快运行速度，减少对数据库的连接次数。

- 自带日志和美化，不需要下载其他插件就可以把日志变色，自动保存日志，这个功能对于爱美的大兄弟简直就 是神仙般的存在（当然也可能只有我喜欢装逼）


- 还有很多......

> 寻找志同道合的朋友一起开发**Aestate**  
> 作者QQ:2075383131(云)  
> qq群：909044439(Aestate Framework)

# 先决条件

> Python >=3.6 (其他版本没试过)  
> 教程文档地址：http://doc.cacode.ren

# 更全面的教程和文档

- [文字教程 doc.cacode.ren](http://doc.cacode.ren)
- [视频教程 bilibili.com](https://www.bilibili.com/video/BV1gq4y1E7Fs/)

# 安装

目前源代码仅开放在gitee，处于组织CACode下，仓库地址为：[aestate](https://gitee.com/aecode/aestate)
使用pip或anaconda安装**Aestate**：

```shell
pip install aestate

conda install aestate 
```

注意请不要用国内镜像下载，只发布在 [pypi.org](https://pypi.org/search/?q=aestate) 也就是pip的官方源下
> qq群：[909044439](https://jq.qq.com/?_wv=1027&k=EK7YEXmh)

# 我是新手，怎么快速入门呢？

你可以前往[https://doc.cacode.ren](https://doc.cacode.ren)跟着官方文档入门  
也可以在B站 [你在写臭虫](https://space.bilibili.com/371089110) 看视频学

# 操作方式太多了一下子学不会怎么办？

**Aestate**有五种方式，不是非要全部都会，我当时写的时候只是为了把很多语言的操作方式用Python实现，然后让其他语言转Python的开发者能够找到熟悉的感觉，例如

1. Java专业户：用xml、方法名和注解
2. Python专业户：用Django模式和SQLAlchemy模式
3. 纯萌新：老老实实写SQL，先把基础练好

# 谁在使用 Aestate Framework 开发网站

CACode： [https://cacode.ren](https://cacode.ren)  
CocoZao 爬虫：[https://ccz.cacode.ren](https://ccz.cacode.ren)
> 开源示例项目：[gitee/aestate-example](https://gitee.com/canotf/aestate-example)

更多示例项目请前往
> [👉 Go to canotf`s homepage on Gitee 👈](https://gitee.com/canotf)

# 鸣谢

Cpython  
DBPool  
Simplejson  
Gitee

# 感谢捐献

<a href="https://gitee.com/spacexzm">
<img alt="Spacexzm" width="49%" src="https://svg.hamm.cn/gitee-user.svg?user=spacexzm"/>
</a>
<a href="https://gitee.com/canotf">
<img alt="Canotf" width="49%" src="https://svg.hamm.cn/gitee-user.svg?user=canotf"/>
</a>

# CACode Development Team
