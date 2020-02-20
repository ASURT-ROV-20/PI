#!/bin/bash

info=`tput setaf 6`
normal=`tput sgr0`
bold=`tput bold`

cd ~
echo ${info}${bold}'Adding sources.list ...'${normal}
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
echo ${info}${bold}'Setup keys ..'${normal}
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
echo ${info}${bold}'Updating packages'${normal}
sudo apt-get update
echo ${info}${bold}'Installing ros'${normal}
sudo apt-get install ros-kinetic-desktop-full
sudo rosdep init
sudo -u $SUDO_USER rosdep update
echo ${info}${bold}"Adding sys vars"${normal}
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
#exec bash
echo ${info}${bold}"installing python dependences"${normal}
sudo apt install -y python-rosinstall python-rosinstall-generator python-wstool build-essential
pip3 install pyyaml
pip3 install rospkg
echo ${info}${bold}"Creating catkin_ws"${normal}
mkdir catkin_ws
sudo chown -R $USER catkin_ws
cd catkin_ws
mkdir src
cd src
echo ${info}${bold}"cloning base repo"${normal}
git clone https://github.com/ASURT-ROV-20/PI
echo ${info}${bold}'Installing rospid'${normal}
sudo apt-get install ros-kinetic-pid

