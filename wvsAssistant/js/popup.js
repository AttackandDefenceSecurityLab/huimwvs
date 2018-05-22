var extension = chrome.extension.getBackgroundPage();
function closePopup() {
    window.close();
}

function test(){
	//console.log("test");
	//closePopup();
}
function stopCapture() {
    closePopup();
    localStorage.captureStatus = 0;
    extension.setInactiveIconInfo();
}
function openOptions() {
    closePopup();
    extension.openOptions();
}
function startCapture() {
    closePopup();
    localStorage.captureStatus = 1;
    extension.setIconInfo();
}

function scanResult(){
	closePopup();
	var scanResultUrl = 'http://203.195.164.69/?id=1';
	//var scanResultUrl = 'http://127.0.0.1/?id=1';
    chrome.tabs.create({
        url: scanResultUrl
    });
}

$(document).ready(function(){
	//console.log("test");
	$("#stopCapture").click(stopCapture);
	$("#startCapture").click(startCapture);
	$("#resultCheck").click(scanResult);
	$("#menuOptions").click(openOptions);
	captureStatus=localStorage.captureStatus;
	if(captureStatus==undefined){
		captureStatus=1;
	}
	//开启的时候，隐藏开启按钮，允许关闭
	if(captureStatus==1){
		$("#startCapture").hide();
	}
	//关闭的时候，隐藏关闭按钮，允许开启
	if(captureStatus==0){
		$("#stopCapture").hide();
	}
})