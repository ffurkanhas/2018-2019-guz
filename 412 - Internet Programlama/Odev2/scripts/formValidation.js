var nameAndSurnameRegEx = /^([a-zA-Z\s\ö\ç\ş\ı\ğ\ü\Ö\Ç\Ş\İ\Ğ\Ü]+)$/;
var nationalIDRegEx = /^([0-9]{11})/;
var studentIDRegEx = /^([0-9]{9})/;
var dateRegEx = /(0[1-9]|[12][0-9]|3[01])[/](0[1-9]|1[012])[/](19|20)\d\d/;
var emailRegEx = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9])+$/;
var passwordRegEx = /^.{1,12}$/;

function validateForm(){
  var nameAndSurname = document.forms["registerForm"]["name"];
  var nationalID = document.forms["registerForm"]["tcKimlik"];
  var studentID = document.forms["registerForm"]["ogrNo"];
  var dateOfBirth = document.forms["registerForm"]["dTarih"];
  var email =  document.forms["registerForm"]["eposta"];
  var password = document.forms["registerForm"]["sifre"];
  var graduated = document.forms["registerForm"]["mezun"];
  var note = document.forms["registerForm"]["note"];
  var flag = 0;

  //nameAndSurname check
  if (nameAndSurname.value == "" || !nameAndSurnameRegEx.test(nameAndSurname.value)){
    nameAndSurname.style.background = "red";
    flag = 1;
  }
  else{
    nameAndSurname.style.background = "yellow";
  }

  //dateOfBirth check
  if (dateOfBirth.value == "" || !dateRegEx.test(dateOfBirth.value)){
    dateOfBirth.style.background = "red";
    flag = 1;
  }
  else{
    dateOfBirth.style.background = "yellow";
  }

  //nationalID check
  if (nationalID.value == "" || !nationalIDRegEx.test(nationalID.value)){
    nationalID.style.background = "red";
    flag = 1;
  }
  else{
    nationalID.style.background = "yellow";
  }

  //studentID check
  if (studentID.value == "" || !studentIDRegEx.test(studentID.value)){
    studentID.style.background = "red";
    flag = 1;
  }
  else{
    studentID.style.background = "yellow";
  }

  //email check
  if (email.value == "" || !emailRegEx.test(email.value)){
    email.style.background = "red";
    flag = 1;
  }
  else{
    email.style.background = "yellow";
  }

  //password check
  if (password.value == "" || !passwordRegEx.test(password.value)){
    password.style.background = "red";
    flag = 1;
  }
  else{
    password.style.background = "yellow";
  }

  //graduated check
  if (graduated.value == ""){
    graduated.value = 'hayir'
  }

  if(flag == 0)
    return true;
  return false;
}
