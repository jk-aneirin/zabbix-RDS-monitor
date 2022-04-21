# zabbix-RDS-monitor
该仓库fork自[XWJR-Ops/zabbix-RDS-monitor](https://github.com/XWJR-Ops/zabbix-RDS-monitor)，但加入了监控RDS-PostgreSQL数据库的支持
   
zabbix通过阿里云api 自动发现、监控阿里云RDS-Mysql和RDS-PostgreSQL数据库      
本版本数据的图表展示，是以**监控项进行分组**。
## 使用方法
### 注意事项
1. 脚本会收集RDS别名，
2. 不要默认别名
3. 不要使用中文别名（zabbix不识别）
4. 切记aliyun-python-sdk-core==2.3.5，新版本的sdk有bug
5. 程序中包含PostgreSQL监控是在数据库使用云盘的情况下，如果你使用本地盘，需要自行修改API参数名，具体参考[阿里云RDS性能参数表](https://help.aliyun.com/document_detail/26316.html)
### 环境要求
python = 2.7
### 模块安装
```shell
/usr/bin/env pip2.7 install aliyun-python-sdk-core==2.3.5 aliyun-python-sdk-rds==2.1.4 datetime
```
### 使用方法
1. 从阿里云控制台获取 **AccessKey** ,并修改脚本中的 **ID** 与 **Secret**
2. 修改区域 **RegionId**
3. 将两个脚本放置于以下目录
```conf
/etc/zabbix/script
```
```shell
chmod +x /etc/zabbix/script/*
```
4. 修改zabbix-agentd.conf，添加以下内容
```conf
#rds
UserParameter=mysql.discovery,/usr/bin/env python2.7 /etc/zabbix/script/discovery_mysql.py
UserParameter=check.mysql[*],/usr/bin/env python2.7 /etc/zabbix/script/check_mysql.py $1 $2 $3
UserParameter=postgre.discovery,/usr/bin/env python2.7 /etc/zabbix/script/discovery_postgre.py
UserParameter=check.postgre[*],/usr/bin/env python2.7 /etc/zabbix/script/check_postgre.py $1 $2 $3
```
5. 重启zabbix-agent
6. zabbix控制台导入模板，并关联主机
