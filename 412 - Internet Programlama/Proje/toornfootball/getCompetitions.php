<?php 
	$competitions_name = array();
	$competitions_value = array();
	$str = file_get_contents('datas/competitions.json');
	$json = json_decode($str, true); 
	foreach ($json as $key1) {
		array_push($competitions_name, $key1['name']);
		array_push($competitions_value, $key1['total_value']);
	}
?>