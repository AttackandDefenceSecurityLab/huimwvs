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
- M去重
    - 机器学习解决DGA式hash
- H sqlmap 暂停终止程序
- MMH hash collision插件
- M csrf插件添加ajax检测
- MH 敏感文件扫描插件

- [x] H多线程
- [x] MHH 扫描结果存入数据库
    - [x]  MHH 数据库连接池
- [x] 扫描器引擎调整
- [x] H php后台展示漏洞数据
- [x] H 插件查看后台数据结果页面

## BUG:
    - SQLMAP中，lib/request/connect.py 588行 raise SqlmapConnectionException(errMsg) 会偶尔导致调用sqlmap的程序也中断
    无法理解，已经抓捕异常了，而且有时候中断，有时候不中断。
    明明已经except:pass了，还是会被中断。
    可以研究有效sqlmap抛出的是什么异常了，就算抛出异常，也被终止。
    这样子，可能是exit语句了。
    暂时把它注释掉，程序先运行着吧。
    算了，先注释就不管了，其中的异常太多了，追寻哪里exit需要时间多，可以用print定位。