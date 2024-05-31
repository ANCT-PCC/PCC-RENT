#!/bin/bash

###############################################################################
# Create setting_files/admin_info.json before run ./install.sh in root user.  #
###############################################################################


docker image build -t pcc-rent:latest . 
docker volume create pcc-rent
docker run --name pcc-rent -p 8080:8080 -d -v ${PWD}:/pcc-rent -t pcc-rent:latest