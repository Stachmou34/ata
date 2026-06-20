<?php
include("../res/x5engine.php");
$nameList = array("ltz","dyt","dmt","kup","64y","pnd","y5d","5zd","85s","545");
$charList = array("K","4","T","N","8","P","T","T","M","X");
$cpt = new X5Captcha($nameList, $charList);
//Check Captcha
if ($_GET["action"] == "check")
	echo $cpt->check($_GET["code"], $_GET["ans"]);
//Show Captcha chars
else if ($_GET["action"] == "show")
	echo $cpt->show($_GET['code']);
// End of file x5captcha.php
