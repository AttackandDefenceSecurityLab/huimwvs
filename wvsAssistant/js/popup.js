function closePopup() {
    window.close();
}

function test(){
	//console.log("test");
	//closePopup();
}

function scanResult(){
	closePopup();
	var scanResultUrl = 'http://203.195.164.69/?id=1';
    chrome.tabs.create({
        url: scanResultUrl
    });
}

$(document).ready(function(){
	//console.log("test");
	$("#resultCheck").click(scanResult);
})