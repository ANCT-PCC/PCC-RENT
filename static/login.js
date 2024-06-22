const $login_button = document.getElementById("loginbutton");
const $form_email = document.getElementById("floatingInput");
const $form_passwd = document.getElementById("floatingPassword");
const $login_status_error = document.getElementById("login_status_error");

const SERVER_ADDR='http://localhost:8081/'

$login_status_error.style.visibility = "hidden";


$login_button.addEventListener('click',(e) => {
    if ($form_email.value == '' || $form_passwd.value == ''){
        $login_status_error.textContent = 'ユーザ名/パスワードを入力してください';
        $login_status_error.style.visibility = 'visible';
    }else{
    var form_data = [
        {uname: String($form_email.value),
        passwd: String($form_passwd.value)
    }
    ];    

    console.log(form_data)
    
    $.ajax(
        {
          url:'http://localhost:8081/'+'login',
          type:'POST',
          data:JSON.stringify(form_data), //ここで辞書型からJSONに変換
          dataType: 'json',
          contentType: 'application/json'
    }).always(function (jqXHR) {
        console.log("statuscode::")
        console.log(jqXHR.status);
        if(String(jqXHR.status) === "200"){
            //ログイン続行
            login_status_error.style.visibility = "hidden";
            window.location.href = 'http://localhost:8081/';
        }else if(String(jqXHR.status) === "444"){
            //入力の修正を求める
            login_status_error.textContent = "認証できませんでした。code="+jqXHR.status;
            login_status_error.style.visibility = "visible";
        }
    });
    }

});