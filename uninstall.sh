#!/bin/bash

docker-compose down
docker rmi pcc-rent-pcc-rent
rm -r mysql/
rm -r my.cnf/
rm -r running/