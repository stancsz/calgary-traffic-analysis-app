#!/bin/bash

# A bash script to start mongodb services


# ps --no-headers -o comm 1
# https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

sudo systemctl start mongod
sudo systemctl status mongod

# if you want to start mongod automatically
#sudo systemctl enable mongod
#sudo systemctl stop mongod