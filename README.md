# IP-Telegram
Send IP to Telegram Bot using Python

## Usage
Clonre repository

### Install module neticaces with
``` sudo apt update ```
``` sudo apt install python3-netifaces ```


### Add to crontab -e
``` @reboot  sleep 60 && /usr/bin/python3 /home/user/ip_telegram1.py > /home/user/my-cron-log.txt ```

ip_telegram1.py works fine on the Raspberry Pi with Pi OS 64 bit 

ip_telegram2.py works fine with the Red Pitaya Board ecosystem 1.04-28 OS 
with Python 3.5 (https://redpitaya.com/rtd-iframe/?iframe=https://redpitaya.readthedocs.io/en/latest/quickStart/SDcard/SDcard.html)

To install crontab on the Red Pitaya STEMlab 125-14:
``` sudo apt-get install cron ```

