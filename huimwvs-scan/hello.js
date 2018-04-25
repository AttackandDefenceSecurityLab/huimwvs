var xss_mark = '6466';
var domxss_mark = '6466domxss';
var xss_exists = 0;
var page = require('webpage').create(),
    sys = require('system'),
    address;

function phantom_exit(message){
    console.log(message);
    setTimeout(function(){
        phantom.exit();
    });
}

page.onConsoleMessage = function(message) {
    console.log('>' + message);
    return true;
};

page.onAlert = function (message) {
    if(message == xss_mark) {
        xss_exists = 1;
        res = "Success:" + message;
        phantom_exit(res);
    }
    console.log('onAlert:' + message);
    return true;
};

page.onConfirm = function(message) {
    console.log('onConfirm:' + message);
    phantom_exit("Success:" + message);
    return true;
};

page.onPrompt = function(message, defaultVal) {
    console.log('onPrompt:' + message);
    phantom_exit("Success:" + message);
    return defaultVal;
};

page.onError = function(message){
    console.log('onError:' + message);
    phantom_exit("Success:" + message);
    return true;
};

phantom.onError = function(message, trace) {
    var msgStack = ['PHANTOM ERROR:' + message];
    if (trace && trace.length) {
        msgStack.push('TRACE:');
        trace.forEach(function(t) {
            msgStack.push(' -> ' + (t.file || t.sourceURL) + ': ' + t.line + (t.function ? ' (in function ' + t.function +')' : ''));
        });
    }
    console.log(msgStack.join('\n'));
    phantom.exit(error);
};

function check_domxss(){
    var xss_mark = '6466';
    var domxss_mark = '6466domxss';
    if(document.getElementsByTagName(domxss_mark).length) {
        alert(xss_mark);
    }
}

function base64decode(j) {
    var h = new Array(-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1);
    var f, d, b, a, e = 0, g = j.length, c = "";
    while (e < g) {
        do {
            f = h[j.charCodeAt(e++) & 255]
        } while (e < g && f == -1);
        if (f == -1) {
            break
        }
        do {
            d = h[j.charCodeAt(e++) & 255]
        } while (e < g && d == -1);
        if (d == -1) {
            break
        }
        c += String.fromCharCode((f << 2) | ((d & 48) >> 4));
        do {
            b = j.charCodeAt(e++) & 255;
            if (b == 61) {
                return c
            }
            b = h[b]
        } while (e < g && b == -1);
        if (b == -1) {
            break
        }
        c += String.fromCharCode(((d & 15) << 4) | ((b & 60) >> 2));
        do {
            a = j.charCodeAt(e++) & 255;
            if (a == 61) {
                return c
            }
            a = h[a]
        } while (e < g && a == -1);
        if (a == -1) {
            break
        }
        c += String.fromCharCode(((b & 3) << 6) | a)
    }
    return c
}


function exec_event(){
    var xss_mark = '6466';
    var domxss_mark = '6466domxss';
    var nodes = document.all;

    for (var i = 0; i < nodes.length; i++) {
        var attrs = nodes[i].attributes;
        for (var j = 0; j < attrs.length; j++) {
            attr_name = attrs[j].nodeName;
            attr_value = attrs[j].nodeValue;
            if (attr_name.substr(0, 2) == 'on') {
                console.log(attrs[j].nodeName + ' : ' + attr_value);
                eval(attr_value);

                if(check_domxss()){
                    alert(xss_mark);
                }
            }

            if(attr_name in {"src": 1, "href": 1} && attrs[j].nodeValue.substr(0,11) == "javascript:"){
                console.log(attrs[j].nodeName + ' : ' + attr_value);
                eval(attr_value.substr(11));

                if(check_domxss()){
                    alert(xss_mark);
                }
            }
        }
    }
    function check_domxss(){
        return document.getElementsByTagName(domxss_mark).length;
    }
}

//main function
if (sys.args.length < 3){
    phantom_exit('Usage: phantomjs hello.js {url} {method} {cookie} {request_data}');
}else {
    // console.log(sys.args[1]);
    address = base64decode(sys.args[1]);
    method = sys.args[2];
    cookie = base64decode(sys.args[3]);
    request_data = base64decode(sys.args[4]);
    console.log(address, method, cookie, request_data);
    }

    if (!address) {
        phantom_exit("Error: Please input Address!(http or https)")
    }
    else if (method.toUpperCase() != "GET" && method.toUpperCase() != "POST") {
        phantom_exit("Error: method must be GET or POST")
    }
    else {
        page.settings = {
            javascriptEnabled: true,
            loadImages: false
        };
        page.open(address, method, cookie, request_data, function (status) {
            if (status !== 'success') {
                console.log('Failed:FAIL to load the address');
            } else {
                if(xss_exists != true){
                    page.evaluateJavaScript(check_domxss.toString());
                    if(xss_exists != true){
                        page.evaluateJavaScript(exec_event.toString());
                        if(xss_exists != true){
                            phantom_exit("End")
                        }
                    }else{
                        phantom_exit("End")
                    }
                }
            }
        }
    )
}
