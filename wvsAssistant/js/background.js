var version = "2.3.2";
var captured;
var request_id = 0;
var request = [];
var requestbody = [];
var filterUrlsEternal = [];
var apihostUserinfo = 'http://client.security.58corp.com/userinfo.php';
var apihostActiveinfo = 'http://client.security.58corp.com/activeinfo.php';
//var apihostScanresult = '203.195.164.69/?id=1';
//var apihost = 'http://203.195.164.69/test.php';
var apihostScanresult = '127.0.0.1/?id=1';
var apihost = 'http://127.0.0.1/test.php';

//启动浏览器时判断插件是否被激活，设置图标
if(localStorage.captureStatus == undefined){
    captured = 1;
}else{
    captured = localStorage.captureStatus;
}

if(captured == 1){
    setIconInfo();
}
else{
    setInactiveIconInfo();
}


var filter = {
    urls: ["<all_urls>"],
    types: [ "main_frame", "sub_frame", "stylesheet", "script", "image", "object", "xmlhttprequest", "other"]
};

console.log("huimwvs Assistant start ");
function captureUrl(reqUrl, method) { //过滤出带参数的请求，去除图片、CSS类没必要检测的请求，以保证检测质量。
    var blacklist=["google.com","baidu.com"];
    for(var h=0;h<blacklist.length;h++){
        if(reqUrl.indexOf(blacklist[h])>=0){
            return 0;
        }
    }
    checktarget=localStorage.checktarget;
    if(reqUrl.indexOf(checktarget)>=0){
        if(method == "POST"){ //POST请求，直接通过
            return 1;
        }else{  //GET请求的处理
        var suffix = [".jpg",".css",".js",".png", ".gif" ,".bmp", ".ico"];
            if(reqUrl.indexOf("?")>=0 && reqUrl.indexOf("=")>=0){  //GET请求带参数
                var domainUrl = reqUrl.split('?');  //检测GET请求的资源格式，JPG CSS JS等不通过
                for (var j = 0; j < suffix.length; j++) {
                    if(domainUrl[0].indexOf(suffix[j])>=0){
                        return 0;
                    }
                }
                return 1;
            }else {
                return 0;
            }
        }
    }
}
//获取post的请求数据，特别含有（POST请求）requestBody部分
chrome.webRequest.onBeforeRequest.addListener(function(details){ //只有onBeforeRequest阶段的details，存在POST数据(requestBody)，在其后该字段会变为requestHeaders
    if(captured == undefined){
        captured = 1;
    }else{
        captured = localStorage.captureStatus;
    }
    if(Number(captured) != 0  && captureUrl(details.url,details.method) != 0){
        var a=1;
    }
    if (Number(captured) != 0 && captureUrl(details.url,details.method) != 0) {
        //if (details.url != apihost && details.url != apihostActiveinfo && details.url != apihostUserinfo) {
        if (details.url != apihostActiveinfo && details.url.indexOf(apihostScanresult)<1 && details.url != apihostUserinfo) {
            id = details.requestId;
            requestbody[id] = details;
            //console.log('POST  '+id + '  '+details['url']);
            //console.log(details);

        }
    }
}, filter, ["blocking", "requestBody"]);

//chrome.webRequest.onBeforeSendHeaders.addListener(function(details{

//}))

//Body与Headers分别于上下两个监听中获取，只能保存两次，并互相取用了。
//获取请求的部分信息，特别含有requestHeaders
//chrome.webRequest.onSendHeaders.addListener(function(details){
chrome.webRequest.onBeforeSendHeaders.addListener(function(details){
    if(captured == undefined){
        captured = 1;
    }else{
        captured = localStorage.captureStatus;
    }
    if(Number(captured) != 0  && captureUrl(details.url,details.method) != 0) {
        request.push(details);
        //console.log(details);
        //console.log("HEADER  "+details['requestId'] + '  '+details['url']);
    }
}, filter, ["requestHeaders"]);

//流量拦截器
//chrome.webRequest.onBeforeRequest.addListener(
//        function(details) { return {cancel: true}; },
//        {urls: ["*://www.baidu.com/*"]},
//        ["blocking"]);

//综合需要的请求数据，发送到服务器
//chrome.webRequest.onHeadersReceived.addListener(function(details){
chrome.webRequest.onSendHeaders.addListener(function(details){
    if(captured == undefined){
        captured = 1;
    }else{
        captured = localStorage.captureStatus;
    }
    //console.log('request_id: '+request_id);
    //console.log("go");
    //console.log("LAST ALL  "+details['requestId'] + '  '+details['url']);
    if(Number(captured) != 0  && captureUrl(details.url,details.method) != 0) {
        var currentreq = request[request_id];
        var requestHeaderLen = currentreq.requestHeaders.length;
        //console.log("request中提取的currentreq.url  " + currentreq.url);
        var reqid = currentreq.requestId;
        //console.log(requestbody[reqid].requestBody);
        if (currentreq.url != apihost && currentreq.url.indexOf(apihost)<1  && currentreq.url != apihostActiveinfo && currentreq.url != apihostUserinfo && currentreq.url.indexOf(apihostScanresult)<1) {
            //console.log("2");
            //console.log("DONE CHECK "+'  '+ currentreq.requestId + '  ' + currentreq.url);
            var reqdic = {};
            for (var i = 0; i < requestHeaderLen; i++) {
                var reqFieldName = currentreq.requestHeaders[i].name;
                var reqfieldValue = currentreq.requestHeaders[i].value;
                reqdic[reqFieldName] = reqfieldValue;
            }
            // captureUrl仅仅对URL进行过滤，这里是对URL外进行全面过滤
            if (currentreq.method == "GET" && currentreq.type != "script" && currentreq.type != "image" && currentreq.type != "stylesheet") {
                //console.log("3");
                var data = {
                    'method':'GET',
                    'url':currentreq.url,
                    'cookie':reqdic['Cookie'],
                    'User-Agent':reqdic['User-Agent'],
                    'refer':reqdic['Referer'],
                    'head':reqdic
                };
                //console.log(data);
            }
            if (currentreq.method == "POST") {
                //console.log("4");
                var reqdata = new Array();
                var reqid = currentreq.requestId;
                //console.log("LAST POST  "+reqid+'  '+currentreq.url);
                //console.log(requestbody[reqid].requestBody.formData);
                try {
                    // console.log(requestbody[reqid].requestBody.formData);
                    // 此处可能报错，出发报错机制：
                    //1. 某些POST请求中没有数据，将导致传入None类型给each函数。
                    //2. 如视频流，发送的为如 raw[0][bytes][[Int8Array]][0]=1，对于对象的集合，length不适用，引发报错
                    //视频流的就不需要发送了。
                    // 此处也杜绝了将无POST数据的POST请求发送给服务器去检测
                    $.each(requestbody[reqid].requestBody.formData, function (name, value) {
                        reqdata.push(name + '=' + value); //将POST参数以 a=b的形式一个个存入数组
                    });
                    var data = {
                        'method':'POST',
                        'url':currentreq.url,
                        'cookie':reqdic['Cookie'],
                        'User-Agent':reqdic['User-Agent'],
                        'refer':reqdic['Referer'],
                        'head':reqdic,
                        'request_data': reqdata.join('&') //将POST数组组成data字符串
                    };
                    //console.log(data);
                }
                catch (e) {
                    console.log(e);
                    //console.log("error");
                }
            }
            if (data) {
                //console.log("5");
                //console.log(data);
                //var currprofile = JSON.parse(localStorage.currentItemProfile);
                console.log(data);
                var pf_ver = "1.0.0";
                $.ajax({
                    url:apihost,
                    type:'POST',
                    data:{
                        //"profilekey":JSON.parse(localStorage.profilekey),
                        "pf_ver": pf_ver,
                        "httpdata":data
                    },
                    crossDomain: 'true',
                    timeout:5000,
                    success: function(response){
                        console.log('---------->> response: ' + JSON.stringify(response));
                    },
                    error: function(XMLHttpRequest,textStatus,errorThrown){
                        console.log('response failed.' + JSON.stringify(XMLHttpRequest));
                    }
                });
                //requestbody.length = 0;
                reqdic.length = 0;
            }
        }
        request_id += 1;
    }
}, filter, ["requestHeaders"]);


//打开配置选项，判断选项页面是否已经打开，如果已经打开就不再打开新标签
function openOptions(firstTime) {
    var url = "options.html";
    if (firstTime)
        url += "?firstTime=true";
    var fullUrl = chrome.extension.getURL(url);
    chrome.tabs.getAllInWindow(null, function(tabs) {
        for (var i in tabs) { // check if Options page is open already
            var tab = tabs[i];
            if (tab.url == fullUrl) {
                chrome.tabs.update(tab.id, { selected: true }); // select the tab
                return;
            }
        }
        chrome.tabs.getSelected(null, function(tab) { // open a new tab next to currently selected tab
            chrome.tabs.create({
                url: url,
                index: tab.index + 1
            });
        });
    });
}

//设置激活图标，即URL右方的图标，用以popup.js调用
function setIconInfo() {
    var title = "";
    var iconPath = "img/128icon.png";
    chrome.browserAction.setIcon({ path: iconPath });
}

//设置停止插件图标，即URL右方的图标，用以popup.js调用
function setInactiveIconInfo() {
    var iconPath = "img/inactive.png";
    var title = "未开启";
    chrome.browserAction.setIcon({ path: iconPath });
}

