![Alt text](SCRIPTS_DEMO_IMAGES/battery_health_notification.jpg)
#### WHAT DOES setup-script.py DO####
# THIS IS A SCHADULED SCRIPT THAT SENDS A POPUP MSG TO THE USER TO TURN OFF THE PC
# 1)-IF IT IS 20% OR LESS [shutdown after 2 mins]
# 2)-IF IT WORKING WHILE IT IS CHARGING [if the user didn't remove the plug shutdown within 2 min in the second time ]

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
