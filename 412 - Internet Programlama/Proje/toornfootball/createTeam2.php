<?php
require_once 'config/config.php';
require_once 'getCompetitions.php';

$sql = "SELECT competition FROM users WHERE username = ?";
$competitionFlag = 0;
    if($stmt = $conn->prepare($sql)){
        $param_username = $_SESSION['username'];
        $stmt->bind_param("s", $param_username);
        
        if($stmt->execute()){
            $stmt->store_result();
            $stmt->bind_result($competition);
            $stmt->fetch();
        } else{
            
        }
    }

$sql = "SELECT player_name FROM users_players WHERE user_id = " . $_SESSION['id'];
$result=mysqli_query($conn,$sql);

$player_names_from_db = array();

while($row = $result->fetch_assoc()){
    array_push($player_names_from_db, $row['player_name']);
}

$sql_player = "SELECT budget FROM users WHERE user_id = " . $_SESSION['id'];

    $stmt = $conn->prepare($sql_player);
    $stmt->execute();
    $stmt->store_result();
    $stmt->bind_result($budget);
    $stmt->fetch();

    $stmt->close();

  $conn->close();

?>

<div class="content">
    <table id="table"" class="table table-condensed table-dark" 
           data-toggle="table"
           data-height="483"
           data-pagination="false"
           data-search="true"
           data-row-style="rowStyle"
           data-url="datas/<? echo $competition ?>.json">
        <thead>
          <tr class="danger">
              <th data-field="name" data-sortable="true">Name</th>
              <th data-field="position" data-sortable="true">Position</th>
              <th data-field="value" data-sortable="true">Total Value</th>
              <th data-field="current_club" data-sortable="true">Current Club</th>
              <th data-field="action" data-formatter="TableActions" data-events="actionEvents">Action</th>
          </tr>
        </thead>
    </table>
</div>

<script type="text/javascript">
    function TableActions (value, row, index) {
            return [
                '<a class="add" href="javascript:void(0)" data-visitorserial="'+row.visitor_id+'" data-visitornames="'+row.visitor_names+'" data-visitorid="'+row.visitor_number+'" title="Add">',
                '<i class="glyphicon glyphicon-plus"></i>',
                '</a>',
                '<a class="remove" href="javascript:void(0)" data-visitorserial="'+row.visitor_id+'" data-visitornames="'+row.visitor_names+'" data-visitorid="'+row.visitor_number+'" title="Remove">',
                '<i class="glyphicon glyphicon-minus"></i>',
                '</a>'
            ].join('');
      }

    var player_names =    <? echo "["; foreach ($player_names_from_db as $p) {
                                    echo "'" . $p . "'," ;
                             }
                              echo "'']";
                              ?>;
    window.actionEvents = {
      'click .add': function (e, value, row, index) {
          var budget = <? echo $budget ?>;

          var element = document.getElementById("table").rows.item(index+1);
          var flag = 0;
          player_names.forEach(function(element) {
            if(element == row['name']){
              flag = 1;
            }
          });
          if(flag == 0){
                if(player_names.length > 15){
                  alert("Already you have 15 players");
                }
                else {
                  if (element.style.color == "red"){
                    alert("Already you have the player");
                  }
                  else{
                    if(row['value'].includes("Th")){
                      var player_value = row['value'].substring(0, row['value'].indexOf(" "));
                      player_value += "000";
                      var int_player_value = parseInt(player_value);
                    }
                    else if(row['value'].includes("Mill")){
                      var player_value = row['value'].substring(0, row['value'].indexOf(","));
                      player_value += "000000";
                      var int_player_value = parseInt(player_value);
                    }
                    if(budget < int_player_value){
                      alert("You do not have money");
                    }
                    else{
                      element.style.color = "red";
                    $.ajax({
                     type: 'POST',
                     url: 'addPlayer.php',
                     data: { 
                        'name' : row['name'],
                        'value': row['value'],
                        'position': row['position'],
                        'current_club': row['current_club']
                     },
                     success: function(response){
                      location.reload();
                     }
                    })
                    }
                  }
                }
                
          }
          else{
            alert("Already you have the player");
          }
          
      },
      'click .remove': function (e, value, row, index) {
          var element = document.getElementById("table").rows.item(index+1);
          flag = 0;
          player_names.forEach(function(element) {
            if(element == row['name']){
              flag = 1;
            }
          });
          if(flag == 1){
                  element.style.color = "black"
                  $.ajax({
                   type: 'POST',
                   url: 'deletePlayer.php',
                   data: { 
                      'name' : row['name'],
                      'value': row['value'],
                      'position': row['position'],
                      'current_club': row['current_club']
                   },
                   success: function(response){
                    location.reload();
                   }
                })
          }
          else{
            alert("You dont have the player");
          }
      }
    };
</script>