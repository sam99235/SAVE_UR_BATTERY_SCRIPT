![Alt text](SCRIPTS_DEMO_IMAGES/battery_health_notification.jpg)
##### what does this script do ???
# THIS IS A SCHADULED SCRIPT THAT SENDS A POPUP MSG TO THE USER TO TURN OFF THE PC
# 1)-IF IT IS 20% OR LESS
[SHUTDOwN IN 2 MINS ]
# 2)-IF the the computer is  ON  WHILE IT'S CHARGING 
[AN ALERT NOTIFICATION WILL BE SENT TO THE  USER TO REMOVE THE PLUG AND THE SECOND TIME IF THE USER DIDN'T REMOVE THE PLUG A SHUTDOWN WILL BE IN 2 MINS]

###setup requirements
python 3.12
### required modules 
##NOTE all these modules come pre-installed with python programme
###if a there is a missing one try to install it using pip3 
win32api
time
subprocess
logging
psutil
winreg
winotify 
