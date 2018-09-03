<?php
require_once 'config/config.php';
session_start();
if(isset($_SESSION['username'])){
    header('location:profile.php');
}
$username = $password = "";
$username_err = $password_err = "";
if($_SERVER["REQUEST_METHOD"] == "POST"){
 
    if(empty(trim($_POST["username"]))){
        $username_err = 'Lütfen kullanıcı adını giriniz';
    } else{
        $username = trim($_POST["username"]);
    }
    
    if(empty(trim($_POST['password']))){
        $password_err = 'Lütfen şifrenizi giriniz';
    } else{
        $password = trim($_POST['password']);
    }

    if(empty($username_err) && empty($password_err)){
        $sql = "SELECT username, password, firstname, lastname, user_id FROM users WHERE username = ?";
        
        if($stmt = $conn->prepare($sql)){
            $stmt->bind_param("s", $param_username);
            
            $param_username = $username;
            
            if($stmt->execute()){
                $stmt->store_result();
                if($stmt->num_rows == 1){                    
                    $stmt->bind_result($username, $hashed_password, $firstname, $lastname, $id);
                    if($stmt->fetch()){
                        if($password == $hashed_password){
                            $_SESSION['username'] = $username;
                            $_SESSION['firstname'] = $firstname;
                            $_SESSION['lastname'] = $lastname;
                            $_SESSION['id'] = $id;
                            header("location: index.php");
                        } else{
                            $password_err = 'Şifre yanlış';
                        }
                    }
                } else{
                    $username_err = 'Kullanıcı adı bulunamadı';
                }
            } else{
                echo "Bir hata oluştu";
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
    <title>Login</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.css">
    <style type="text/css">
        body{ font: 14px sans-serif;}
        .wrapper{ width: 350px; padding: 20px; margin: auto;}
    </style>
</head>
<body>
    <div class="wrapper">
        <h2>Giriş</h2>
        <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
            <div class="form-group <?php echo (!empty($username_err)) ? 'has-error' : ''; ?>">
                <label>Kullanıcı Adı</label>
                <input type="text" name="username"class="form-control" value="<?php echo $username; ?>">
                <span class="help-block"><?php echo $username_err; ?></span>
            </div>    
            <div class="form-group <?php echo (!empty($password_err)) ? 'has-error' : ''; ?>">
                <label>Şifre</label>
                <input type="password" name="password" class="form-control">
                <span class="help-block"><?php echo $password_err; ?></span>
            </div>
            <div class="form-group">
                <input type="submit" class="btn btn-primary" value="Login">
            </div>
            <p><a href="register.php">Kayıt olmak için tıklayınız</a></p>
        </form>
    </div>    
</body>
</html>