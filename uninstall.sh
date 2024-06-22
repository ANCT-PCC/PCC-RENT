#!/bin/bash

docker-compose stop
docker rm pcc-rent
docker rm pcc-rent-db
docker rmi pcc-rent-pcc-rent