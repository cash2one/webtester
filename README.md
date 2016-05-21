#浏览器兼容性自动化测试平台
##概览
基于selenium的网页浏览器兼容性自动化测试平台，Web服务基于Python Django
##浏览器支持
* IE
* FirFox
* Chrome
* Opera
* Safari

##系统支持
* Windows 10
* Windows 8
* Windows 7
* Windows vista
* Windos xp
* Linux with x11 (不支持更改分辨率）
* OS X （不支持更改屏幕分辨率）

##部署环境
###web服务部署
* 操作系统：Web服务并不需要桌面运行环境，所以你可以选择任何主流的服务器操作系统，只要它支持Django和NodeJS
* Web服务器：生产力环境下需要支持支持wsgi，推荐使用httpd
* 数据库：Mysql
* 其他要求 redis Nodejs Python >=2.7 安装所需python模块

```bash
$git clone https://github.com/liuyajun52/webtester
$cd webtester
$sh build.sh
$cp webtester/setting.py.template webtester/setting.py  #修改数据库配置，另外还需在mysql中建立相应数据库
$python manage.py migrate #初始化数据库表
$vim webtester/setting.py 
$sh start-web.sh
```

###测试机部署
* 操作系统：同系统支持
* 浏览器：安装所需测试浏览器，下载对应selenium webdriver，在path下可见
* 其他要求 python >=2.7 安装所需模块
* 将webtester/setting.py.template webtester/setting.py 并修改配置

```python
#web服务部署机器的redis地址，这里可以使用内网ip或公网ip或域名
BROKER_URL = 'redis://localhost:6379/0'

#web服务部署机器的域名或ip（内网或公网）
WEB_MATER_HOST='localhost'
#web服务部署端口
WEB_MASTER_PORT=8080
```

```cmd
>git clone https://github.com/liuyajun52/webtester
>cd webtester
>start-tester.bat
```