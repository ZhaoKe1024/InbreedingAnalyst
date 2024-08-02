[English](./README_cn.md)  | 简体中文

通过网页录制音频、填写信息，通过Javascript 发送POST到Python Flask框架，然后存储到MySQL数据库，音频存储到本地文件，两者通过文件名对应。

# 最小所需文件结构
只需如下三个文件
```
root
└─main.py  # 运行启动flask服务
└─templates
│    └─index.html  # 前端页面
└─databasekits
     └─table_packets.py
```
其他都不必要。


# 运行MySQL
```
systemctl start mysqld
```

运行Python Flask
```
python3 main.py
```

查询
```
> sudo mysql -uroot -p
> {password}
> {password}
> use {databsename}
> select * from {tablename}
```
