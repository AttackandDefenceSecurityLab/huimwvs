var version = "2.3.2";
var captured;
var request_id = 0;
var request = [];
var requestbody = [];
var filterUrlsEternal = [];
var apihostUserinfo = 'http://client.security.58corp.com/userinfo.php';
var apihostActiveinfo = 'http://client.security.58corp.com/activeinfo.php';
var apihost = 'http://127.0.0.1/test.php';

var filter = {
    urls: ["<all_urls>"],
    types: [ "main_frame", "sub_frame", "stylesheet", "script", "image", "object", "xmlhttprequest", "other"]
};

console.log("OK");
function captureUrl(reqUrl, method) { //过滤出带参数的请求，去除图片、CSS类没必要检测的请求，以保证检测质量。
    var whilelist=["google.com","baidu.com"];
    for(var h=0;h<whilelist.length;h++){
        if(reqUrl.indexOf(whilelist[h])>=0){
            return 0;
        }
    }
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
//获取post的请求数据，特别含有（POST请求）requestBody部分
chrome.webRequest.onBeforeRequest.addListener(function(details){ //只有onBeforeRequest阶段的details，存在POST数据(requestBody)，在其后该字段会变为requestHeaders
    captured=1;
    if(captureUrl(details.url,details.method) != 0){
        var a=1;
    }
    if (Number(captured) != 0 && captureUrl(details.url,details.method) != 0) {
        if (details.url != apihost && details.url != apihostActiveinfo && details.url != apihostUserinfo) {
            id = details.requestId;
            requestbody[id] = details;
        }
    }
}, filter, ["blocking", "requestBody"]);

//Body与Headers分别于上下两个监听中获取，只能保存两次，并互相取用了。
//获取请求的部分信息，特别含有requestHeaders
chrome.webRequest.onSendHeaders.addListener(function(details){
    captured=1;
    if(Number(captured) != 0  && captureUrl(details.url,details.method) != 0) {
        request.push(details);
        //console.log(details);
    }
}, filter, ["requestHeaders"]);

//综合需要的请求数据，发送到服务器
chrome.webRequest.onHeadersReceived.addListener(function(details){
    captured=1;
    //console.log("go");
    if(Number(captured) != 0){
        //console.log("OK-1");
    }
    if(captureUrl(details.url,details.method) != 0){
        //console.log("OK-2");
    }
    if(Number(captured) != 0  && captureUrl(details.url,details.method) != 0) {
        //console.log("1");
        var currentreq = request[request_id];
        var requestHeaderLen = currentreq.requestHeaders.length;
        if (currentreq.url != apihost && currentreq.url != apihostActiveinfo && currentreq.url != apihostUserinfo) {
            //console.log("2");
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
                try {
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
}, filter, ["blocking", "responseHeaders"]);