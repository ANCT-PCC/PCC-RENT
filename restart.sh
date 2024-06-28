#!/bin/bash

docker-compose down
docker rmi pcc-rent-pcc-rent
docker-compose up -d