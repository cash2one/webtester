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
$sh start-web.sh
```


###测试机部署
* 操作系统：同系统支持
* 浏览器：安装所需测试浏览器，下载对应selenium webdriver，在path下可见
* 其他要求 python >=2.7 安装所需模块

```cmd
>git clone https://github.com/liuyajun52/webtester
>cd webtester
>start-tester.bat
```