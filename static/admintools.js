const SERVER_ADDR = 'http://localhost:8080/'
const $DB_DOUNLOAD = document.getElementById('dbdl_button');

$DB_DOUNLOAD.addEventListener('click',(e)=>{

    $.ajax({
        url:SERVER_ADDR+'admintools/pcc-rent.db',
        type:'GET',
        dataType: 'json'
    }).always()
})