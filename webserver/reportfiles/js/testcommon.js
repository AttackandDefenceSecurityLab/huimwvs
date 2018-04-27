//更改主界面连接
function GetLeftUrl (url) {
	window.parent.frames["mainFrame"].window.location.href = url;
}
//隐藏和显示
function hideAndShow (showID, hideID) {
	document.getElementById(showID).style.display = '';
	document.getElementById(hideID).style.display = 'none';
}
//隐藏或显示
function hideOrShow (itemID) {
	var Item = document.getElementById(itemID);
	if (Item.style.display == "") {
		Item.style.display = "none";
	}else {
		Item.style.display = "";
	}
}
//带图片的隐藏和显示
function hideBodyImg (hide_id, imgID, hide_image, show_image) {
	var hide_item = document.getElementById(hide_id);
	var img = document.getElementById(imgID);
	if (hide_item.style.display == "") {
		hide_item.style.display = "none";
		img.src = hide_image;
	}else {
		hide_item.style.display = "";
		img.src = show_image;
	}
}
//编辑状态开关
function DisableBody (edit_id) {
	var edit_item = document.getElementById(edit_id);
	if (edit_item.disabled == true) {
		edit_item.disabled = false;
	}else {
		edit_item.disabled = true;
	}
}
//创建新窗口
function CreateNewWindow (openUrl, windowName, widthNum, heightNum) {
	var winObj = window.open(openUrl, windowName, "width=" + widthNum + ", height=" + heightNum + ",toolbar=no, directories=no, status=no, scrollbars=yes");
}
//全屏显示
function FullScreen (item_id) {
	if (item_id.value == "全屏显示") {
		item_id.value = "取消全屏";
		window.parent.leftMenu.style.display = "none";
		window.parent.topMenu.style.display = "none";
	}else {
		item_id.value = "全屏显示";
		window.parent.leftMenu.style.display = "";
		window.parent.topMenu.style.display = "";
	}
}
function more_toggle(o,id,same_bg) {
		var tr_more=document.getElementById(id);
		var tr_class=(o.parentNode.parentNode.className!=""&&same_bg)?(" "+o.parentNode.parentNode.className):"";
		if (tr_more.className=="more hide"||tr_more.className=="more hide"+tr_class) {
			o.className="ico minus";
			tr_more.className="more"+tr_class;
		}
		else {
			o.className="ico plus";
			tr_more.className="more hide"+tr_class;
		}
};
function showTab(o,n) {
		var tabs = o.parentNode.parentNode.getElementsByTagName("li");
		for (i = 0; i < tabs.length; i++) {
			tabs[i].className = "select";
		}
		tabs[n].className = "selected";
		var con = o.parentNode.parentNode.parentNode.getElementsByTagName("div");
		for (i = 0; i < con.length; i++) {
			con[i].className = "tab_content hide";
		}
		con[n].className = "tab_content";
		return false;
}

(function($){
	$.fn.report_tree = function(options){
		var defaults = {}
		var options = $.extend(defaults, options);
		this.each(function(){
			$(this).find("a.dot").bind("click",function(){
			if($(this).hasClass('up')){$(this).removeClass('up').addClass("down").nextAll('ul').hide();}
			else if($(this).hasClass('down')){$(this).removeClass('down').addClass("up").nextAll('ul').show();}
			else return false;
			})	
		});
	};
	$.fn.catalog = function(options){
		var defaults = {"title":"title"}
		var options = $.extend(defaults, options);
		var c_log=function(_ul,_id,_p){
			_id.find(">div.report_h").each(function(i){
			var li=$("<li></li>").appendTo(_ul);
			var _s=$(this);
			_s.attr("id",_p+String(i));
			var _h=$("<a class='dot'></a><a class='link' href='#"+_p+String(i)+"'>"+_s.html()+"</a>").appendTo(li)
			var _sc=_s.next("div.report_content");
			if(_sc.find(">div.report_h").length){
			var cl=(_p+String(i)).length-options.title.length>1? "down":"up";
			li.find("a.dot").addClass(cl).bind("click",function(){
			if($(this).hasClass('up')){$(this).removeClass('up').addClass("down").nextAll('ul').hide();}
			else if($(this).hasClass('down')){$(this).removeClass('down').addClass("up").nextAll('ul').show();}
			else return false;
			});
			var _2ul=$("<ul style='display:"+(cl=='down'?'none':'')+"'></ul>").appendTo(li);
			c_log(_2ul,_sc,_p+String(i));
			}
			});
			$("#catalog").find("a.link").bind("click",function(){
				$("#catalog").find("div.report_content").hide();
				$("#catalog").find(".h1_dot").addClass("up");
			});
			return _ul;
		};
		this.each(function(){
			var _s=$(this)
			var _c=_s.find("#catalog");
			var _co=$("<div class='report_content' style='display:none'><ul id='catalog_tree'></ul></div>").appendTo(_c);
			var _h=_s.find("#content");
			_co=_s.find("#catalog_tree");
			c_log(_co,_h,options.title);
			var _a=$("<a class='h1_dot'></a>").appendTo(_s.find(".report_h1"));
			$(_a[0]).addClass("up");
			_s.find(".report_h1").click(function(){
			$(this).next("div.report_content").toggle();
			$(this).find(".h1_dot").toggleClass("up");
			});
			var _a2=$("<a class='h2_dot'></a>").appendTo(_s.find(".report_h2"));
			_s.find(".report_h2").click(function(){
			$(this).next("div").toggle();
			$(this).find(".h2_dot").toggleClass("up");
			});
		});
	};
	
})(jQuery);
(function($){
	$.gotop=function(id){
		if(window!=parent){
			var dom=document,__a=dom.createElement("div");
			__a.style.cssText="display:none;";
			__a.innerHTML="<a title='Back to top' class='gotop' onfoucs='this.blur()'  onclick='scroll(0,0);return false'  href='"+(id||"#")+"'></a>";
			dom.body.appendChild(__a);
			__a.style.display=="none"&&(document.onscroll=function(){
				__a.style.display="";
			});
		}
		else {
		$.gotop._aTop=$("<a title='Back to top' class='gotop' onfoucs='this.blur()' style='display:none' href='"+(id||"#")+"'></a>").appendTo($('body'));
		var _dalay=setTimeout(function(){
			$(window).scrollTop()>100? $.gotop._aTop.css('display','block'):$.gotop._aTop.hide();
			if($.browser.msie && $.browser.version<7){$.gotop._aTop.attr("class","gotop")};
		},1000);
		$(window).scroll(function(){
			clearTimeout(_dalay);
			var _dalay=setTimeout(function(){
			$(window).scrollTop()>100? $.gotop._aTop.css('display','block'):$.gotop._aTop.hide();
			if($.browser.msie && $.browser.version<7){$.gotop._aTop.attr("class","gotop")};
			},1000);
			
			if($("#content").offset().top<=$(window).scrollTop()) 
			{
				$("#catalog").addClass("fixed_top");
				$("#catalog").css('width',$("#report").width());
			}
			else
			{
				$("#catalog").removeClass("fixed_top");
			}
		});
		}
	};
  })(jQuery);
jQuery(function($){
	//window.dialog = new UI.Dialog({name:'dialog'});
	$("#catalog_tree").report_tree();
	$("#report").catalog();
	$.gotop();
});

function no_toggle(oid,id) {
	if (jQuery('#'+oid).hasClass('ico')){
		if (jQuery('#'+oid).hasClass('plus')) {
			jQuery('#'+oid).removeClass('plus');
			jQuery('#'+oid).addClass('minus');
		}
		else {
			jQuery('#'+oid).removeClass('minus');
			jQuery('#'+oid).addClass('plus');	
		}
	}
		jQuery('#'+id).toggle();
};
