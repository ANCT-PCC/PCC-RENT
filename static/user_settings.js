const $logout_button = document.getElementById('logout_button');
const $changePWD_button = document.getElementById('changePWD_button');
const $changeSuccess = document.getElementById('changeSuccess');
const $changeFailed = document.getElementById('changeFailed');
const $newPWD = document.getElementById('newPWD');
const $newPWD_retype = document.getElementById('newPWD_retype');
const $currentPWD = document.getElementById('currentPWD');

function init(){
  $changeFailed.style.visibility = 'hidden';
  $changeSuccess.style.visibility = 'hidden';
  $currentPWD.value = '';
  $newPWD.value = '';
  $newPWD_retype.value = '';
};

$changePWD_button.addEventListener('click',(e)=>{
  currentPWD = $currentPWD.textContent;
  newPWD = $newPWD.value;
  newPWD_retype = $newPWD_retype.value;

  if (newPWD != newPWD_retype){
    $changeSuccess.style.visibility = 'hidden';
    $changeFailed.innerText = "新しいパスワードが一致しません";
    $changeFailed.style.visibility = 'visible';

    $currentPWD.value = '';
    $newPWD.value = '';
    $newPWD_retype.value = '';
  }else{
    $changeFailed.style.visibility = 'hidden';
    $changeSuccess.innerText = "パスワードが変更されました";
    $changeSuccess.style.visibility = 'visible';

    $currentPWD.value = '';
    $newPWD.value = '';
    $newPWD_retype.value = '';
  };
  
});

init()