#!/bin/bash
echo "This script assumes you're using a UNIX user of 'clocktower' and are in the directory 'SimpleClocktower'"
read -p "Continue? (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

echo "Installing ClockTower"

apt install python3
apt install python3-pip3
apt install pipenv

pipenv install

pip install pygame
pip install parse

echo ""
echo "Finished installing ClockTower dependencies"
echo ""

mkdir ./Songs/
mkdir ./Songs/Test
mkdir ./Songs/Daily
mkdir ./Songs/Daily/hhmm
mkdir ./Songs/DayOfWeek/
mkdir ./Songs/DayOfWeek/1_Sunday
mkdir ./Songs/DayOfWeek/1_Sunday/hhmm
mkdir ./Songs/DayOfWeek/2_Monday
mkdir ./Songs/DayOfWeek/2_Monday/hhmm
mkdir ./Songs/DayOfWeek/3_Tuesday
mkdir ./Songs/DayOfWeek/3_Tuesday/hhmm
mkdir ./Songs/DayOfWeek/4_Wednesday
mkdir ./Songs/DayOfWeek/4_Wednesday/hhmm
mkdir ./Songs/DayOfWeek/5_Thursday
mkdir ./Songs/DayOfWeek/5_Thursday/hhmm
mkdir ./Songs/DayOfWeek/6_Friday
mkdir ./Songs/DayOfWeek/6_Friday/hhmm
mkdir ./Songs/DayOfWeek/7_Saturday
mkdir ./Songs/DayOfWeek/7_Saturday/hhmm
mkdir ./Songs/Date/
mkdir ./Songs/Date/yyyy-mm-dd
mkdir ./Songs/Date/yyyy-mm-dd/hhmm
# Give full permissions for Samba edits
chmod -R 777 ../SimpleClocktower

echo ""
echo "Finished creating ClockTower song directories"
echo ""

# Run clockTower script every minute
(crontab -u clocktower -l ; echo "* * * * * cd /home/clocktower/SimpleClocktower/ && python3 ./clockTower.py") | crontab -u clockTower -
echo ""
echo "Added Cron Job to run ClockTower every minute"

echo ""
echo "Setting up new hostname 'clocktower'"
echo ""
sed -i 's/\(.*\)raspberrypi/\1clocktower/g' /etc/hosts
sed -i 's/raspberrypi/clocktower/g' /etc/hostname

echo ""
echo "Setting up file share"
sudo apt install samba samba-common-bin
sed -i '/workgroup = WORKGROUP$/a wins support = yes' /etc/samba/smb.conf
sed -i '/wins support = yes$/a security = user' /etc/samba/smb.conf
echo ""
echo "[Clocktower]" >> /etc/samba/smb.conf
echo " comment=Clocktower files" >> /etc/samba/smb.conf
echo " path=/home/clocktower/SimpleClocktower" >> /etc/samba/smb.conf
echo " read only=no" >> /etc/samba/smb.conf
echo " valid users=clocktower" >> /etc/samba/smb.conf
echo " create mask=0777" >> /etc/samba/smb.conf
echo " directory mask=0777" >> /etc/samba/smb.conf

echo ""
echo "Setting up new samba user 'clocktower'"
smbpasswd -a clocktower

echo ""
echo "Setup Complete! Rebooting in 10 seconds.  Press <Enter> to reboot now"
read -n 1 -t 10
reboot