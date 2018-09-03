<?php
require_once 'config/config.php';
require_once 'getCompetitions.php';
$sql = "SELECT player_name, current_club, value, position FROM users_players WHERE user_id = " . $_SESSION['id'];
        $result=mysqli_query($conn,$sql);

        $player_names_from_db = array();
        $player_position = array();
        $player_value = array();
        $player_current_club = array();

        while($row = $result->fetch_assoc()){
            array_push($player_names_from_db, $row['player_name']);
            array_push($player_position, $row['position']);
            array_push($player_value, $row['value']);
            array_push($player_current_club, $row['current_club']);
        }

if($_SERVER["REQUEST_METHOD"] == "POST"){
  $name = $_POST['name'];

  $sql_player = "SELECT budget FROM users WHERE user_id = " . $_SESSION['id'];

    $stmt = $conn->prepare($sql_player);
    $stmt->execute();
    $stmt->store_result();
    $stmt->bind_result($budget);
    $stmt->fetch();

  $sql_player = "SELECT value FROM users_players WHERE player_name=? and user_id =? ";

    $stmt = $conn->prepare($sql_player);
    $stmt->bind_param("si", $name, $_SESSION['id']);
    $stmt->execute();
    $stmt->store_result();
    $stmt->bind_result($value);
    $stmt->fetch();

  $bosluk = " ";
  $virgul = ",";

  $value = 0;

  if(isset($value)){
      if (strpos($value, 'Th.') !== false) {
        $boslukIndex = strpos($value, $bosluk);
        $value = substr($value, 0, $boslukIndex) . "000";
      }

      if (strpos($value, 'Mill.') !== false) {
        $virgulIndex = strpos($value, $virgul);
        $value = substr($value, 0, $virgulIndex) . "000000";
      }
  }
  
  $result_budget = $budget + $value;

  $sql = "UPDATE users SET budget= ? WHERE username = ?";
  $param_username = $_SESSION['username'];

  $stmt = $conn->prepare($sql);
  $stmt->bind_param("is", $result_budget, $param_username);
  $stmt->execute();

  $sql = "DELETE FROM users_players WHERE user_id=? and player_name = ?";

  $stmt = $conn->prepare($sql);
  $stmt->bind_param("is", $_SESSION['id'], $name);
  $stmt->execute();
}

?>
<div class="content">
  <table class="table table-striped table-bordered table-hover" id="dataTables-example">
      <thead>
          <tr>
              <th>Name</th>
              <th>Position</th>
              <th>Value</th>
              <th>Current Club</th>
              <th>Delete</th>
          </tr>
      </thead>
      <tbody>
        <?php for ($i = 0; $i < count($player_names_from_db); $i++) { ?>
            <tr>
              <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
                <td><?php echo $player_names_from_db[$i]; ?></td>
                <td><?php echo $player_position[$i]; ?></td>
                <td><?php echo $player_value[$i]; ?></td>
                <td><?php echo $player_current_club[$i]; ?></td>
              
                <td><input type="submit" class="btn btn-primary" value="<?php echo $player_names_from_db[$i]; ?>" name="name"></td>
              </form>
            </tr>
        <?php } ?>
      </tbody>
  </table>
</div>