<?php
require_once 'config/config.php';
require_once 'getCompetitions.php';
session_start();
if(isset($_SESSION['username'])){
    header('location:profile.php');
}
$username = $firstname = $lastname = $password = $confirm_password = "";
$username_err = $firstname_err = $lastname_err = $password_err = $confirm_password_err = "";
 
if($_SERVER["REQUEST_METHOD"] == "POST"){

    $selected_competition = $_POST["competition_control"];
 
    if(empty(trim($_POST["username"]))){
        $username_err = "Lütfen kullanıcı adını giriniz";
    } else{
        $sql = "SELECT user_id FROM users WHERE username = ?";
        
        if($stmt = $conn->prepare($sql)){
            $stmt->bind_param("s", $param_username);
                
            $param_username = trim($_POST["username"]);
            
            if($stmt->execute()){
                $stmt->store_result();
                
                if($stmt->num_rows == 1){
                    $username_err = "Bu kullanıcı adı daha önce alınmıştır.";
                } else{
                    $username = trim($_POST["username"]);
                }
            } else{
                echo "Bir hata oluştu";
            }
        }
        $stmt->close();
    }
    
    // Validate password
    if(empty(trim($_POST['password']))){
        $password_err = "Lütfen bir şifre giriniz.";     
    } else{
        $password = trim($_POST['password']);
    }

    if(empty($_POST['firstname'])){
        $firstname_err = "Lütfen isminizi giriniz.";     
    } else{
        $firstname = trim($_POST['firstname']);
    }

    if(empty($_POST['lastname'])){
        $lastname_err = "Lütfen soy isminizi giriniz.";     
    } else{
        $lastname = trim($_POST['lastname']);
    }
    
    // Validate confirm password
    if(empty(trim($_POST["confirm_password"]))){
        $confirm_password_err = 'Lütfen şifrenizi giriniz.';     
    } else{
        $confirm_password = trim($_POST['confirm_password']);
        if($password != $confirm_password){
            $confirm_password_err = 'Şifreler uyuşmamakta';
        }
    }
    
    if(empty($username_err) && empty($password_err) && empty($confirm_password_err) && empty($firstname_err) && empty($lastname_err)){

        $sql = "INSERT INTO users (username, password, firstname, lastname, reg_date, permission_level, competition) VALUES (?, ?, ?, ?, ?, ?, ?)";
         
        if($stmt = $conn->prepare($sql)){
            $stmt->bind_param("sssssss", $param_username, $param_password, $param_firstname, $param_lastname, $param_reg_date, $param_permission_level, $param_competition);

            $param_username = $username;
            $param_password = $password;
            $param_firstname = $firstname;
            $param_lastname = $lastname;
            $param_reg_date = date("Y-m-d H:i:s");
            $param_permission_level = 1;
            $param_competition = $competitions_name[$selected_competition];
            
            if($stmt->execute()){
                header("location: login.php");
            } else{
                echo "Hata oluştu tekrar deneyiniz.";
            }
        }
        $stmt->close();
    }
    $conn->close();
}
?>
 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Toorn Blogger</title>
    <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css" rel="stylesheet" id="bootstrap-css">
	<script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/js/bootstrap.min.js"></script>
	<script src="//code.jquery.com/jquery-1.11.1.min.js"></script>
    <style type="text/css">
        body{ font: 14px sans-serif; }
        .wrapper{ width: 350px; padding: 20px; margin: auto;}
    </style>
</head>
<body>
    <?php  ?>
    <div class="wrapper">
        <h2>Kayıt Formu</h2>
        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
            <div class="form-group <?php echo (!empty($username_err)) ? 'has-error' : ''; ?>">
                <label>Kullanıcı Adı</label>
                <input type="text" name="username" class="form-control" value="<?php echo $username; ?>">
                <span class="help-block"><?php echo $username_err; ?></span>
            </div> 
            <div class="form-group <?php echo (!empty($firstname_err)) ? 'has-error' : ''; ?>">
                <label>Adınız</label>
                <input type="text" name="firstname" class="form-control" value="<?php echo $firstname; ?>">
                <span class="help-block"><?php echo $firstname_err; ?></span>
            </div>   
            <div class="form-group <?php echo (!empty($lastname_err)) ? 'has-error' : ''; ?>">
                <label>Soyadınız</label>
                <input type="text" name="lastname" class="form-control" value="<?php echo $lastname; ?>">
                <span class="help-block"><?php echo $lastname_err; ?></span>
            </div>  
            <div class="form-group <?php echo (!empty($password_err)) ? 'has-error' : ''; ?>">
                <label>Şifre</label>
                <input type="password" name="password" class="form-control" value="<?php echo $password; ?>">
                <span class="help-block"><?php echo $password_err; ?></span>
            </div>
            <div class="form-group <?php echo (!empty($confirm_password_err)) ? 'has-error' : ''; ?>">
                <label>Şifre Doğrulama</label>
                <input type="password" name="confirm_password" class="form-control" value="<?php echo $confirm_password; ?>">
                <span class="help-block"><?php echo $confirm_password_err; ?></span>
            </div>
            <div class="form-group">
                <select name="competition_control" class="form-control">
                <? $i = 0; foreach ($competitions_name as $competition_) { ?>
                    <option value="<? echo $i ?>"><? echo $competition_; ?></option>
                <? $i++; } ?>
            </select>
            <div class="form-group" class="form-control">
                <input type="submit" class="btn btn-primary" value="Kayıt Ol">
                <input type="reset" class="btn btn-default" value="Temizle">
            </div>
            <p style="margin-top:5px;"><a href="login.php">Bir hesabınız var mı?</a></p>
        </form>
    </div>
</body>
</html>