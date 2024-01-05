const $login_button = document.getElementById("loginbutton");
var $form_email = document.getElementById("floatingInput");
var $form_passwd = document.getElementById("floatingPassword");

$login_button.addEventListener('click',(e) => {

    console.log("DEBUG POINt");


    var form_data = [
        {uname: String($form_email.value),
        passwd: String($form_passwd.value),
        'Access-Control-Allow-Origin': '*',
    }
    ];    
    
    $.ajax(
        {
          url:'http://localhost:443/login_phase',
          type:'POST',
          data:JSON.stringify(form_data), //ここで辞書型からJSONに変換
          dataType: 'json',
          contentType: 'application/json'
    }).always(function (jqXHR) {
        console.log(jqXHR.status);
    })

});