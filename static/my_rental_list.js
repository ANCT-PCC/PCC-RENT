const SERVER_ADDR = 'http://localhost:8080/'
const $logout_button = document.getElementById('logout_button');


/*ページ(DOM)読み込み後に実行*/
window.onload = function(){

    //tbodyのIDを取得(この中で処理します)
    var tbody = document.getElementById('item-table');

    $.ajax(
      {
        url:SERVER_ADDR+'show_my_rental_list',
        type:'GET',
        dataType: 'json',
        async: 'false'
      }).done(function(json){
        var data=JSON.stringify(json);
        var res = JSON.parse(data);

        for (i = 0; i < res.length; i++){
          //tr エレメントを新規作成(ただ生成するだけ)
          var tr = document.createElement('tr');
          
          //列(td)用のループ
          for (j = 0; j < 6; j++){
              //tdエレメントをを生成
              var td = document.createElement('td');
              //tdの中に入れたいモノをセット
              if(j == 0){
                td.innerHTML = res[i]['number']
              }else if(j== 1){
                td.innerHTML = res[i]['item_name']
              }else if(j==2){
                td.innerHTML = res[i]['use']
              }else if(j==3){
                td.innerHTML = res[i]['rent']
              }else if(j==4){
                td.innerHTML = res[i]['deadline']
              }else if(j==5){
                if(res[i]['returned'] == '貸し出し中'){
                  td.innerHTML = res[i]['returned']+"<br>"+"<button type='button' class='btn btn-primary'>返却</button>";
                }else{
                  td.innerHTML = 'insertError'
                }
                
              }
              //生成したtdをtrにセット
              tr.appendChild(td);
              
          }//列用のループ閉じ
          //tr エレメントをtbody内に追加(ここではじめて表示される)
          tbody.appendChild(tr);
  
        }//行用のループ閉じ

      }).fail(function(){
        console.log("failed")
      });

};
