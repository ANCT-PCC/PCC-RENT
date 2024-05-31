#!/bin/bash

cp pcc-rent.db ../pcc-rent-DB-backup/
echo "****Use GitHub Account which joined ANCT-PCC Organization !****"
git pull
./reinstall.sh