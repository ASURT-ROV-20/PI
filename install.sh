#!/bin/bash

info=`tput setaf 5`
success=`tput setaf 2`
error=`tput setaf 1`
normal=`tput sgr0`
bold=`tput bold`

cd install

echo "${info}${bold}Installing ROS${normal}"
sudo ./ross_install.sh
if [ $? -eq 0 ]; then
    echo "${success}${bold}ROS Installed Successfully${normal}"
else
    echo "${error}${bold}Failed to install ROS${normal}"
fi

echo "${info}${bold}Installing GST${normal}"
sudo ./gst_install.sh
if [ $? -eq 0 ]; then
    echo "${success}${bold}GST Installed Successfully${normal}"
else
    echo "${error}${bold}Failed to install GST${normal}"
fi

echo "${info}${bold}Installing Hardware Libs${normal}"
sudo ./hardware.sh
if [ $? -eq 0 ]; then
    echo "${success}${bold}Hardware Libs Installed Successfully${normal}"
else
    echo "${error}${bold}Failed to install Hardware Libs${normal}"
fi