<!DOCTYPE html>
<html>
<head>
</head>
<body>
<?php 
  session_start();
  if(!isset($_SESSION['username'])){
   header('location:login.php');
  }
  else{
    header('location:profile.php');
  }
?>
</body>
</html>
