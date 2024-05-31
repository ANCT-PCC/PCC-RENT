#!/bin/bash

###############################################################################
# Create setting_files/admin_info.json before run ./install.sh in root user.  #
###############################################################################

sed -e s#http://localhost:8080/#http://192.168.200.100:8080/#g static/login.js > static/login.js
sed -e s#http://localhost:8080/#http://192.168.200.100:8080/#g static/admin-db.js > static/admin-db.js
sed -e s#http://localhost:8080/#http://192.168.200.100:8080/#g static/admin-user.js > static/admin-user.js
sed -e s#http://localhost:8080/#http://192.168.200.100:8080/#g static/admin-item.js > static/admin-item.js
sed -e s#http://localhost:8080/#http://192.168.200.100:8080/#g static/admin-top.js > static/admin-top.js
sed -e s#http://localhost:8080/#http://192.168.200.100:8080/#g static/admintools.js > static/admintools.js
sed -e s#http://localhost:8080/#http://192.168.200.100:8080/#g static/dashboard.js > static/dashboard.js
sed -e s#http://localhost:8080/#http://192.168.200.100:8080/#g static/members.js > static/members.js
sed -e s#http://localhost:8080/#http://192.168.200.100:8080/#g static/my_rental_list.js > static/my_rental_list.js
sed -e s#http://localhost:8080/#http://192.168.200.100:8080/#g static/passwd_change.js > static/passwd_change.js
sed -e s#http://localhost:8080/#http://192.168.200.100:8080/#g static/pcc-items.js > static/pcc-items.js
sed -e s#http://localhost:8080/#http://192.168.200.100:8080/#g static/user_settings.js > static/user_settings.js

docker image build -t pcc-rent:latest . 
docker volume create pcc-rent
docker run --name pcc-rent -p 8080:8080 -v ${PWD}:/pcc-rent -t pcc-rent:latest