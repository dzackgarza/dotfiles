#!/bin/bash

echo "Installing MESA3D dependencies..."
yum -y install mesa-libGL-devel mesa-libGLU-devel mesa-libOSMesa-devel llvm-devel glx-utils-7.11-5.el6.x86_64 

echo "Installing x11 dependencies..."
yum -y install xorg-x11-xauth xorg-x11-server-devel xorg-x11-server-Xvfb-1.10.6-1.0.1.el6.centos.x86_64 xorg-x11-server-Xorg-1.10.6-1.el6.centos.x86_64
