<?php

$DB_SERVER = 'localhost';
$DB_USERNAME = 'root';
$DB_PASSWORD = '';
$DB_NAME = 'toornfootball';
// Connect to MySQL
$conn = new mysqli($DB_SERVER, $DB_USERNAME, $DB_PASSWORD);
if($conn != null){
    $create_database_query = "CREATE DATABASE IF NOT EXISTS " . $DB_NAME;
    if($result = $conn->query($create_database_query)){
      $table_check_query = "SELECT user_id FROM users";
      $conn->select_db($DB_NAME);
      if(!$result = $conn->query($table_check_query)){
        $create_table_query = "CREATE TABLE users (
          user_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
          username VARCHAR(30) NOT NULL,
          firstname VARCHAR(30) NOT NULL,
          lastname VARCHAR(30) NOT NULL,
          password VARCHAR(30) NOT NULL,
          competition VARCHAR(250) DEFAULT NULL,
          budget INT DEFAULT 5000000,
          reg_date TIMESTAMP,
          permission_level int
        )";
        if(!$result = $conn->query($create_table_query)){
          echo "Create users table error";
        }
        else{
        }
      }
    } else {
        echo "Create database error";
    }


    $table_check_query_players = "SELECT id FROM users_players";
    $conn->select_db($DB_NAME);


    if(!$result = $conn->query($table_check_query_players)){
      $create_table_query2 = "CREATE TABLE IF NOT EXISTS users_players (
          player_id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
          user_id INT(6) UNSIGNED NOT NULL,
          FOREIGN KEY (user_id) REFERENCES users(user_id),
          player_name VARCHAR(250) NOT NULL,
          current_club VARCHAR(250),
          value VARCHAR(250),
          position VARCHAR(50)
        )";
        if(!$result = $conn->query($create_table_query2)){
          echo "Create users_players table error";
        }
    }
}
else{
  echo "Database connection error" . mysqli_connect_errno();
}
?>
