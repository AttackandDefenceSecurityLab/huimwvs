var extension = chrome.extension.getBackgroundPage();
function saveOptions() {
    var infos = $('#batch-add').val();
    //点击保存时改变颜色为灰色，用户明白“已经保存”
    $("#batch-add").css("background-color","#F0F0F0");
    localStorage.checktarget=infos;
    console.log(localStorage.checktarget);
    
}

function closeWindow() {
    if (confirm("是否保存更改？")){
        saveOptions();
    }
    window.close();
}
document.addEventListener('DOMContentLoaded', function() {
    $("#profileSave").click(saveOptions);
    $("#batch-add").click(function(){
        $("#batch-add").css("background-color","#FFFFFF");
    });
    //点击Input时改变颜色为白色，用户明白“正在修改”
    $("#btnClose").click(function () {
        closeWindow();
    });
       
});


