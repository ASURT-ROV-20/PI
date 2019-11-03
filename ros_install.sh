  GNU nano 2.5.3                                            File: setup.sh                                                                                               

cd ~
echo 'Adding sources.list ...'
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
echo 'Setup keys ..'
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
echo 'Updating packages'
sudo apt-get update
echo 'Installing ros'
sudo apt-get install ros-kinetic-desktop-full -y
sudo rosdep init
rosdep update
echo "Adding sys vars"
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
exec bash
echo "installing python dependences"
sudo apt install python-rosinstall python-rosinstall-generator python-wstool build-essential -y
echo "Creating catkin_ws"
mkdir catkin_ws/src
cd catkin_ws
catkin_make
echo "configuering catkin_ws"
cd devel
path=$(pwd)
path=$path"/setup.bash"
echo "source $path" >> ~/.bashrc
source ~/.bashrc
exec bash
cd ../src
echo "cloning base repo"
git clone https://github.com/ASURT-ROV-20/PI
cd PI




