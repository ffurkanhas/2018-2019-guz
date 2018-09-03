<?php

$curl_handle=curl_init();
curl_setopt($curl_handle, CURLOPT_URL,'https://www.transfermarkt.com/live/index?datum=2018-07-23');
curl_setopt($curl_handle, CURLOPT_CONNECTTIMEOUT, 2);
curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($curl_handle, CURLOPT_USERAGENT, 'transfermarktResultScraper');
$query = curl_exec($curl_handle);
curl_close($curl_handle);

$pokemon_doc = new DOMDocument;
libxml_use_internal_errors(true);
$pokemon_doc->loadHTML($query);
libxml_clear_errors();
$pokemon_xpath = new DOMXPath($pokemon_doc);

$ev_sahipleri = $pokemon_xpath->query('//table[@class="livescore"]//td[@class="verein-heim"]');
$rakipler = $pokemon_xpath->query('//table[@class="livescore"]//td[@class="verein-gast"]');
$sonuclar = $pokemon_xpath->query('//table[@class="livescore"]//span[@class="matchresult finished"]');

echo "<div class='content'>";

for ($x = 0; $x < count($sonuclar); $x++) {
	echo $ev_sahipleri[$x]->nodeValue, " ", $sonuclar[$x]->nodeValue , " ", $rakipler[$x]->nodeValue ,"<br>";
}

echo "</div>";
?>