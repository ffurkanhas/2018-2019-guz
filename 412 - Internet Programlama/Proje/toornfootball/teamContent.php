<?php
require_once 'config/config.php';
require_once 'getCompetitions.php';

$sql = "SELECT competition FROM users WHERE username = ?";
$competitionFlag = 0;
    if($stmt = $conn->prepare($sql)){
        $stmt->bind_param("s", $param_username);
        
        $param_username = $_SESSION['username'];
        
        if($stmt->execute()){
            $stmt->store_result();
            $stmt->bind_result($competition);
            
        } else{
            echo "Bir hata oluştu";
        }
    }
    $stmt->close();

  $conn->close();

?>


<div class="content">
</div>