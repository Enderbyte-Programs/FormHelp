<?php

$title = $_GET["name"] or die("ERR!!");
$path = "../helps/" . $title;

$file = fopen($path,"r");
$data = fread($file, filesize($path));
fclose($file);

echo $data;//Print the page contents