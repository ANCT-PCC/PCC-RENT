const $login_button = document.getElementById("loginbutton");
const $form_email = document.getElementById("floatingInput");
const $form_passwd = document.getElementById("floatingPassword");
const $login_status_error = document.getElementById("login_status_error");

$login_status_error.style.visibility = "hidden";


$login_button.addEventListener('click',(e) => {

    var form_data = [
        {uname: String($form_email.value),
        passwd: String($form_passwd.value),
    }
    ];    
    
    $.ajax(
        {
          url:'http://localhost:443/login',
          type:'POST',
          data:JSON.stringify(form_data), //ここで辞書型からJSONに変換
          dataType: 'json',
          contentType: 'application/json'
    }).always(function (jqXHR) {
        console.log(jqXHR.status);
        if(String(jqXHR.status) === "200"){
            //ログイン続行
        }else if(String(jqXHR.status) === "4545"){
            //入力の修正を求める
          login_status_error.textContent = "ユーザ名/パスワードに誤りがあります。";
          login_status_error.style.visibility = "visible";
        }else{
            //入力の修正を求める
          login_status_error.textContent = "管理者を呼べ。非常事態だ";
          login_status_error.style.visibility = "visible";
        }
    });

});