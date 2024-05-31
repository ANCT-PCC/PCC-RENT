#!/bin/bash

mkdir ../pcc-rent-Backup
docker cp pcc-rent:/PCC-RENT/pcc-rent.db ../pcc-rent-Backup
docker cp pcc-rent:/PCC-RENT/setting_files ../pcc-rent-Backup
echo "****Use GitHub Account which joined ANCT-PCC Organization !****"
git pull
./reinstall.sh