function closePopup() {
    window.close();
}

function test(){
	//console.log("test");
	//closePopup();
}

function scanResult(){
	closePopup();
	var scanResultUrl = 'http://127.0.0.1/?id=1';
    chrome.tabs.create({
        url: scanResultUrl
    });
}

$(document).ready(function(){
	//console.log("test");
	$("#resultCheck").click(scanResult);
})