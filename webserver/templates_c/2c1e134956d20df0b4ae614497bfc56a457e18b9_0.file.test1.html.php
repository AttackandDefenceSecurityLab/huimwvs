<?php
/* Smarty version 3.1.32, created on 2018-04-27 23:11:05
  from 'E:\phpStudy\WWW\templates\test1.html' */

/* @var Smarty_Internal_Template $_smarty_tpl */
if ($_smarty_tpl->_decodeProperties($_smarty_tpl, array (
  'version' => '3.1.32',
  'unifunc' => 'content_5ae33d89e37631_14934904',
  'has_nocache_code' => false,
  'file_dependency' => 
  array (
    '2c1e134956d20df0b4ae614497bfc56a457e18b9' => 
    array (
      0 => 'E:\\phpStudy\\WWW\\templates\\test1.html',
      1 => 1524841864,
      2 => 'file',
    ),
  ),
  'includes' => 
  array (
  ),
),false)) {
function content_5ae33d89e37631_14934904 (Smarty_Internal_Template $_smarty_tpl) {
?><!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>huimwvs报表</title>
<link rel="stylesheet" href="reportfiles/css/ns_report.css" />
<link rel="stylesheet" href="reportfiles/css/ns_report_rsas.css" />
<link rel="stylesheet" href="reportfiles/js/datepicker/skin/WdatePicker.css" />
<?php echo '<script'; ?>
 src="reportfiles/js/jquery.js"><?php echo '</script'; ?>
>
<?php echo '<script'; ?>
 src="reportfiles/js/common.js"><?php echo '</script'; ?>
>
<?php echo '<script'; ?>
 src="reportfiles/js/datepicker/WdatePicker.js"><?php echo '</script'; ?>
>
</head>
<body>
<div id="report" class="wrapper_w800">
  <div  id="head"  class="report_title">
    <h1>huimwvs报表</h1>
    <span class="note">&nbsp;</span> </div>
  <!--head end,catalog start-->


  <div>
    <table id="vuln_distribution" class="report_table">
    <thead>
    <tr class="second_title">
        <th style='width:40px'>序号</th>
        <th >目标</th>
        <th style='width:150px'>漏洞类型</th>

    </tr>
    </thead>
    <tbody>



<?php
$_smarty_tpl->tpl_vars['num'] = new Smarty_Variable(null, $_smarty_tpl->isRenderingCache);$_smarty_tpl->tpl_vars['num']->step = 1;$_smarty_tpl->tpl_vars['num']->total = (int) ceil(($_smarty_tpl->tpl_vars['num']->step > 0 ? $_smarty_tpl->tpl_vars['datacount']->value-1+1 - (0) : 0-($_smarty_tpl->tpl_vars['datacount']->value-1)+1)/abs($_smarty_tpl->tpl_vars['num']->step));
if ($_smarty_tpl->tpl_vars['num']->total > 0) {
for ($_smarty_tpl->tpl_vars['num']->value = 0, $_smarty_tpl->tpl_vars['num']->iteration = 1;$_smarty_tpl->tpl_vars['num']->iteration <= $_smarty_tpl->tpl_vars['num']->total;$_smarty_tpl->tpl_vars['num']->value += $_smarty_tpl->tpl_vars['num']->step, $_smarty_tpl->tpl_vars['num']->iteration++) {
$_smarty_tpl->tpl_vars['num']->first = $_smarty_tpl->tpl_vars['num']->iteration === 1;$_smarty_tpl->tpl_vars['num']->last = $_smarty_tpl->tpl_vars['num']->iteration === $_smarty_tpl->tpl_vars['num']->total;?>    
    <tr class="odd vuln_high" style="cursor:pointer;" onclick="no_toggle('4_1_<?php echo $_smarty_tpl->tpl_vars['num']->value+1;?>
','table_4_1_<?php echo $_smarty_tpl->tpl_vars['num']->value+1;?>
')">
        <td><?php echo $_smarty_tpl->tpl_vars['num']->value+1;?>
</td>
        <td>
        <img id="4_1_1" class="ico plus" src="reportfiles/images/blank.gif">
        <img align='absmiddle' src='reportfiles/images/vuln_high.gif' ></img>
        <span style='color:#E42B00'><?php echo $_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['target'];?>
</span>
        </td>
        <td><?php echo $_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['vultype'];?>
</td>
    </tr>
    <tr class="more hide odd" id="table_4_1_<?php echo $_smarty_tpl->tpl_vars['num']->value+1;?>
">
        <th></th>
        <td style="padding-left:20px" class="extend" colspan='2'>
            <table style="white-space:pre-wrap;" class="report_table" width="100%">
				<?php $_smarty_tpl->_assignInScope('ident', 0);?>
				
				<?php if (isset($_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['plugin_author'])) {?>
				<tr class="<?php echo $_smarty_tpl->tpl_vars['ident_arr']->value[$_smarty_tpl->tpl_vars['ident']->value];
$_smarty_tpl->_assignInScope('ident', ($_smarty_tpl->tpl_vars['ident']->value+1)%2);?>">
					<th width="15%">[插件作者]</th>
					<td width="85%"><?php echo $_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['plugin_author'];?>
</td>
				</tr>
				<?php }?>
				
				<?php if (isset($_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['target']) || isset($_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['vultype'])) {?>
				<tr class="<?php echo $_smarty_tpl->tpl_vars['ident_arr']->value[$_smarty_tpl->tpl_vars['ident']->value];
$_smarty_tpl->_assignInScope('ident', ($_smarty_tpl->tpl_vars['ident']->value+1)%2);?>">
					<th>[风险]</th>
					<td>目标 <?php echo $_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['target'];?>
  存在 <?php echo $_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['vultype'];?>
 </td>
				</tr>
				<?php }?>
				
				<?php if (isset($_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['para'])) {?>
				<tr class="<?php echo $_smarty_tpl->tpl_vars['ident_arr']->value[$_smarty_tpl->tpl_vars['ident']->value];
$_smarty_tpl->_assignInScope('ident', ($_smarty_tpl->tpl_vars['ident']->value+1)%2);?>">
					<th>[参数]</th>
					<td><?php echo $_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['para'];?>
</td>
				</tr>
				<?php }?>
				
				<?php if (isset($_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['descrip'])) {?>
				<tr class="<?php echo $_smarty_tpl->tpl_vars['ident_arr']->value[$_smarty_tpl->tpl_vars['ident']->value];
$_smarty_tpl->_assignInScope('ident', ($_smarty_tpl->tpl_vars['ident']->value+1)%2);?>">
					<th>[详细说明]</th>
					<td><?php echo $_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['descrip'];?>
</td>
				</tr>
				<?php }?>
				
				<?php if (isset($_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['severity'])) {?>
				<tr class="<?php echo $_smarty_tpl->tpl_vars['ident_arr']->value[$_smarty_tpl->tpl_vars['ident']->value];
$_smarty_tpl->_assignInScope('ident', ($_smarty_tpl->tpl_vars['ident']->value+1)%2);?>">
					<th>[危害等级]</th>
					<td><?php echo $_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['severity'];?>
</td>
				</tr>
				<?php }?>
				
				<?php if (isset($_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['vultype'])) {?>
				<tr class="<?php echo $_smarty_tpl->tpl_vars['ident_arr']->value[$_smarty_tpl->tpl_vars['ident']->value];
$_smarty_tpl->_assignInScope('ident', ($_smarty_tpl->tpl_vars['ident']->value+1)%2);?>">
					<th>[漏洞类型]</th>
					<td><?php echo $_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['vultype'];?>
</td>
				</tr>
				<?php }?>
				
				<?php if (isset($_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['payload'])) {?>
				<tr class="<?php echo $_smarty_tpl->tpl_vars['ident_arr']->value[$_smarty_tpl->tpl_vars['ident']->value];
$_smarty_tpl->_assignInScope('ident', ($_smarty_tpl->tpl_vars['ident']->value+1)%2);?>">
					<th>[漏洞POC]</th>
					<td><?php echo $_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['payload'];?>
</td>
				</tr>
				<?php }?>
				
				<?php if (isset($_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['ref'])) {?>
				<tr class="<?php echo $_smarty_tpl->tpl_vars['ident_arr']->value[$_smarty_tpl->tpl_vars['ident']->value];
$_smarty_tpl->_assignInScope('ident', ($_smarty_tpl->tpl_vars['ident']->value+1)%2);?>">
					<th>[相关引用]</th>
					<td><?php echo $_smarty_tpl->tpl_vars['rows']->value[$_smarty_tpl->tpl_vars['num']->value]['ref'];?>
</td>
				</tr>
				<?php }?>
				
    
            </table>
        </td>
	</tr>
	<?php }
}
?>
	</tbody>
	<tfoot>
    </tfoot>
    </table>
  </div></div></div>
  </div>
</div>
<!--content end-->
</div>
</body>
</html>
<?php }
}
