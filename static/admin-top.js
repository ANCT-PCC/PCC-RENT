const SERVER_ADDR = 'http://localhost:8080/'
const $MOVE_DB = document.getElementById('move_db')
const $MOVE_ITEM = document.getElementById('move_item')

window.onload = function(){

    $MOVE_DB.addEventListener('click',(e)=>{
        window.location = SERVER_ADDR+'admintools/db'
    })
    
    $MOVE_ITEM.addEventListener('click',(e)=>{
        window.location = SERVER_ADDR+'admintools/item'
    })
}