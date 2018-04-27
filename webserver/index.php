<?php
require './libs/Smarty.class.php';
$smarty=new Smarty();




//header("Content-type: text/html; charset=utf-8"); 
include("./sql-connections/sql-connect.php");
$rows=array();
$datacount=0;
$ident_arr=array("old","even");
$smarty->assign('ident_arr',$ident_arr);
if(isset($_GET['id'])){
	$id=$_GET['id'];
	$sql="SELECT * FROM vul";
	//echo $sql;
	
	mysql_query("SET NAMES 'UTF8'");
	$result=mysql_query($sql);
	
	
	
	$i=0;
	while($row=mysql_fetch_array($result)){
		if(isset($row['payload'])){
			$row['payload']=str_replace("[cut-off]","</br>",$row['payload']);
		}
		if(isset($row['ref'])){
			$row['ref']=str_replace("[cut-off]","</br>",$row['ref']);
		}
		
		$rows[$i]=$row;
		$i++;
	}
	$smarty->assign('rows',$rows);
	$datacount=count($rows);
	$smarty->assign('datacount',$datacount);
}
$smarty->display('./test1.html');

