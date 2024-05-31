#!/bin/bash

docker cp pcc-rent:/PCC-RENT/pcc-rent.db ../pcc-rent-Backup/pcc-rent.db
docker cp pcc-rent:/PCC-RENT/setting_files ../pcc-rent-Backup/setting_files
echo "****Use GitHub Account which joined ANCT-PCC Organization !****"
git pull
./reinstall.sh