# huimwvs
## 一 wvsAssistant
#### 截取转发游览器流量到扫描器服务器的chrome插件

## 二 huimwvs-scan
#### 扫描器引擎以及扫描插件
数据库环境
- [DBUtils] pip install DBUtils
- MySQLdb

## 三 webserver
#### php服务器端
- 接收wvsAssistant数据并存入redis的程序。
- 额外需要环境：phpredis





## 四 待进行
- L sqlmap优化
- M xss插件
    - 存储型与DOM XSS检测
- H php后台展示漏洞数据
- H 插件查看后台数据结果页面
- MMH hash collision插件
- M csrf插件添加ajax检测
- MH 敏感文件扫描插件

- [x] MHH 扫描结果存入数据库
    - [x]  MHH 数据库连接池
    - [x] 扫描器引擎调整