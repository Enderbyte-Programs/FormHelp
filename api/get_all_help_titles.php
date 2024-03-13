<?php
error_reporting(E_ALL);
ini_set('display_errors', '1');

$helpdir = "../helps";
foreach (scandir($helpdir) as $file) {
    if ($file == "."|| $file == "..") continue;

    if (is_dir($helpdir ."/". $file)) {
        continue;
    }

    $filen = fopen($helpdir ."/". $file,"r");
    $line = fgets($filen);
    $sline = str_split($line);
    fclose($filen);
    //Read first line (which should be title line of file)
    
    $loffset = 0;
    $llen = count($sline);
    $line = trim($line);
    if (str_starts_with($line,"<!--")) {
        $loffset = 4;
        $llen -= 4;
    }
    if (str_ends_with($line,"-->"))  {
        $loffset = 4;
        $llen -= 5;
    }
    //COnfigure slice to trim HTML comments if found

    $title = array_slice($sline,$loffset,$llen);//-4 for first HTML comment, -7 to trim end of html comment. Only if needed
    echo join($title) . ";;" .  $file . "``";
}