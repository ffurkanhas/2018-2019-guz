<?php
  require_once 'config/config.php';
  require_once 'getCompetitions.php';
  session_start();

	$name = $_POST['name'];
	$value = $_POST['value'];
	$position = $_POST['position'];
	$current_club = $_POST['current_club'];
	$bosluk = " ";
	$virgul = ",";

	if (strpos($value, 'Th.') !== false) {
    	$boslukIndex = strpos($value, $bosluk);
    	$value = substr($value, 0, $boslukIndex) . "000";
	}

	if (strpos($value, 'Mill.') !== false) {
    	$virgulIndex = strpos($value, $virgul);
    	$value = substr($value, 0, $virgulIndex) . "000000";
	}

	$sql_player = "SELECT budget FROM users WHERE user_id = " . $_SESSION['id'];

	  $stmt = $conn->prepare($sql_player);
	  $stmt->execute();
	  $stmt->store_result();
	  $stmt->bind_result($budget);
	  $stmt->fetch();

    $int_value = (int) $value;

    $result_budget = $budget - $int_value;

	$sql = "UPDATE users SET budget= ? WHERE username = ?";
	$param_username = $_SESSION['username'];

	$stmt = $conn->prepare($sql);
    $stmt->bind_param("is", $result_budget, $param_username);
    $stmt->execute();

	$sql = "INSERT INTO users_players VALUES (0 , ?, ?, ?, ?, ?)";

	$stmt = $conn->prepare($sql);
    $stmt->bind_param("issss", $_SESSION['id'], $name, $current_club, $value, $position);
    $stmt->execute();

?>