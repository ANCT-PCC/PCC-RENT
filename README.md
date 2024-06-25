# 備品管理システム「PCC-RENT」
## どんなシステム
・備品を管理するよ  
・全ユーザ/ユーザごとに借用履歴を表示できるよ  
・「借りた」「返した」の通知はDiscordでお知らせ！  
・弊部の基幹認証システム「PCC-CAS」のアカウントを使うよ  
・学内ネットワークからしかアクセスできないと不便なので、サーバは開発者(Discord: networld4816)の専用環境で動かしてるよ  
・Cloudflare tunnnelを活用しているよ  

## セットアップ方法
1, Ubuntu ServerにDocker-composeを入れる  
2, Cloudflare Tunnelをセットアップする  
3, Releaseから最新バージョンを落とす  
4, 専用ディレクトリでファイルを解凍  
5, ./install.sh を実行  
6, docker ps で動作確認  
7, 事前に設定したCloudflareのアドレスにアクセスして  
8, ページが表示されればOK

## 開発環境
MacBook Air 13 M2  
VSCode  
Python3.10.11  
とかいろいろ。
## 開発者問い合わせ
Discord: networld4816  
Twitter (旧X): networld4816