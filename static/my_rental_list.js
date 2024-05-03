
const $logout_button = document.getElementById('logout_button');


/*ページ(DOM)読み込み後に実行*/
window.onload = function(){

    //tbodyのIDを取得(この中で処理します)
    var tbody = document.getElementById('item-table');

    var bgcolorFlag = 0;
    for (i = 0; i < 5; i++){
        //tr エレメントを新規作成(ただ生成するだけ)
        var tr = document.createElement('tr');
        //列(td)用のループ
        for (j = 0; j < 6; j++){
            //tdエレメントをを生成
            var td = document.createElement('td');
            //tdの中に入れたいモノをセット
            if(j == 0){
              td.innerHTML = i
            }else if(j== 1){
              td.innerHTML = "備品名 "+i
            }else if(j==2){
              td.innerHTML = "色々なことに使う"
            }else if(j==3){
              td.innerHTML = "無期限★"
            }else if(j==4){
              td.innerHTML = "なし"
            }else if(j==5){
              td.innerHTML = "<a href='https://www.google.com' target='_blank'>写真</a>"
            }
            //生成したtdをtrにセット
            tr.appendChild(td);
        }//列用のループ閉じ
        //tr エレメントをtbody内に追加(ここではじめて表示される)
        tbody.appendChild(tr);

    }//行用のループ閉じ

};
