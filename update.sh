#!/bin/bash

docker-compose stop
docker rm pcc-rent
docker rmi pcc-rent-pcc-rent

git pull
docker-compose up -d
docker ps