#!/bin/bash
PREV_ADDR='http://localhost:8081/'
#SERVER_ADDR='https://pcc-rent.nemnet-lab.net/' #本番環境
SERVER_ADDR='http://localhost:8081/' #試験環境

#CAS_SERVER_ADDR='https://pcc-cas.nemnet-lab.net/' #本番環境
CAS_SERVER_ADDR='http:localhost:8081' #試験環境

sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/login.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/admin-db.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/admin-user.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/admin-item.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/admin-top.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/admintools.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/dashboard.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/members.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/my_rental_list.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/passwd_change.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/pcc-items.js
sed -i -e s#$PREV_ADDR#$SERVER_ADDR#g static/user_settings.js

sed -i -e s#http://127.0.0.1:8080/#$CAS_SERVER_ADDR#g templates/user_settings.html

python run.py
