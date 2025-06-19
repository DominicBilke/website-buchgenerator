<?php

function curl_file_get_contents($url){
$curl_handle=curl_init();
curl_setopt($curl_handle, CURLOPT_URL,$url);
curl_setopt($curl_handle, CURLOPT_CONNECTTIMEOUT, 0);
curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($curl_handle, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0');
$result = curl_exec($curl_handle);
curl_close($curl_handle);
return $result;
}

ini_set('default_socket_timeout', 1200);
set_time_limit(0);

$ctx = stream_context_create(array('http'=>
    array(
        'timeout' => 1200,  //1200 Seconds is 20 Minutes
    )
));


$_GET['Thema'] = str_replace('.html', '', $_GET['Thema']);

if(isset($_GET['Vorwort'])) {
	file_put_contents('./uploads/'.$_GET['Thema'].'_vorwort.html', nl2br(curl_file_get_contents("https://askgpt.bilke-projects.com/ask.php?".http_build_query(array("ask" => 'Schreibe ein ausführliches Vorwort für das Thema '.$_GET['Thema'])))));
	echo $_GET['Thema'].'_vorwort.html';
}
else if(isset($_GET['Nachwort'])) {
	file_put_contents('./uploads/'.$_GET['Thema'].'_nachwort.html', nl2br(curl_file_get_contents("https://askgpt.bilke-projects.com/ask.php?".http_build_query(array("ask" => 'Schreibe ein ausführliches Nachwort für das Thema '.$_GET['Thema'])))));
	echo $_GET['Thema'].'_nachwort.html';
}


else if(isset($_GET['Thema'])) {
	file_put_contents('./uploads/'.$_GET['Thema'].'.html', curl_file_get_contents("https://askgpt.bilke-projects.com/topic.php?".http_build_query(array("ask" => $_GET['Thema']))));
	echo $_GET['Thema'].'.html';
}
?>