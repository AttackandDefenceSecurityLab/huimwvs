<?php
if(isset($_POST['httpdata'])){
$data=$_POST['httpdata'];
}
//echo $result;
//实例化redis
$redis = new Redis();
//连接
$redis->connect('127.0.0.1', 6379);

//判断是否为重复，刚开始置1
$ifDuplicate=1;



$arr=explode("?",$data['url']);
$url=$arr[0];

$newparas="";

if(isset($data['request_data'])){
	$paras = explode("&",$data['request_data']);
	for($x=0;$x<count($paras);$x++){
		$para=explode("=",$paras[$x]);
		$check=$url.'?POST'.$para[0];
		$add_result = $redis->sadd('duplication',$check);
		if($add_result == True){
			$newparas .= $para[0];
			$ifDuplicate=0;
		}
	}
}

//判断是否有GET参数
//只有出现新参数，才会存入LIST中
if(count($arr)>1){
	$paras = explode("&",$arr[1]);
	for($x=0;$x<count($paras);$x++){
		$para=explode("=",$paras[$x]);
		$check=$url.'?GET'.$para[0];
		$add_result = $redis->sadd('duplication',$check);
		if($add_result == True){
			$newparas .= '&'.$para[0];
			$ifDuplicate=0;
		}
	}
}

//将新出现的参数记录入新元素中，以帮助某些插件如sqli xss减少工作量
if($newparas != ""){
	$data['newparas']=substr($newparas,1);
	//print_r($data);
}

//将json对象转换为字符串存入redis
$result=json_encode($data);
//存数据
//取数据时使用 lrange，先进先出，旧数据先检测
if($ifDuplicate==0){
	$redis->rpush('data',$result);
	echo "NEW MESSAGE!SAVE";
}
else{
	echo "EXISTED!";
}

?>