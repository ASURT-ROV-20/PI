#!/bin/bash

info=`tput setaf 6`
normal=`tput sgr0`
bold=`tput bold`
echo ${info}${bold}"configuering catkin_ws"${normal}

cd ~/catkin_ws
catkin_make
cd devel
path=$(pwd)
path=$path"/setup.bash"
echo "source $path" >> ~/.bashrc
source ~/.bashrc
