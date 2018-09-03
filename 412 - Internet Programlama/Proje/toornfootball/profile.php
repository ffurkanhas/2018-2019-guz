<?php 
  require_once 'config/config.php';
  require_once 'getCompetitions.php';
  session_start();

  if($_SERVER["REQUEST_METHOD"] == "POST"){
  	$selected_competition = $_POST["competition_control"];
  	$selected_competition_name = $competitions_name[$selected_competition];

	$sql = "UPDATE users SET competition= ? WHERE username = ?";
	$param_username = $_SESSION['username'];

	$stmt = $conn->prepare($sql);
    $stmt->bind_param("ss", $selected_competition_name, $param_username);
    $stmt->execute();

  }
?>
<html>
<head>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
	<!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.12.1/bootstrap-table.min.css">

	<!-- Latest compiled and minified JavaScript -->
	<script src="//cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.12.1/bootstrap-table.min.js"></script>

	<!-- Latest compiled and minified Locales -->
	<script src="//cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.12.1/locale/bootstrap-table-zh.min.js"></script>
	<link rel="stylesheet" href="styles/styles.css"/>
	<title><?php 
		if(!isset($_SESSION['username'])){
			header('location:login.php');
		}
		else{
			echo $_SESSION['firstname'] . " " . $_SESSION['lastname'] . "'s Team";
		}
	?></title>
	<style type="text/css">
		body {
			font-family: Arial;
		}
	</style>
</head>
<body>
<?php
  if(!isset($_SESSION['username'])){
   header('location:login.php');
  }
  else{
    include 'navigation_bar.php';
    include 'menu.php';
  }
?>
	<div class="content">
		<form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
	        <select name="competition_control">
		        <? $i = 0; foreach ($competitions_name as $competition_) { ?>
		            <option value="<? echo $i ?>"><? echo $competition_; ?></option>
		        <? $i++; } ?>
	    	</select>
	    	<input type="submit" value="Change">
	    </form>
	</div>
</body>
</html>