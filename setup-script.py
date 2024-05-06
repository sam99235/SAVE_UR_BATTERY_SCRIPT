# script by mejdoubi oussama
#### WHAT DOES THIS SCRIPT DO####
# THIS IS A SCHADULED SCRIPT THAT SENDS A POPUP MSG TO THE USER TO TURN OFF THE PC
# 1)-IF IT IS 20% OR LESS [shutdown after 2 mins]
# 2)-IF IT WORKING WHILE IT IS CHARGING [if the user didn't remove the plug shutdown within 2 min in the second time ]

# dev notes
# TO DO LIST
# if the logging file is bigger then an X bytes in size // has been used 4 7-days do an automatic clean up
# time on the log file isn't formatted well
# schedule the scipt using task schceduler api
# create the save_your_key on registry key in the script
# push the script in ur git repo put readme, requiremets
# need the isplugged key to be created using winreg module to push it in the hithub repo
# use a friendly-ui for the user + bug report + contact email
# use python -m pip install NAME instead of pip if the same error persists
# check pep8 and coding best practices
# 1) if the user didn't see the popup the shutdown  must occur after 3 mins
# set a setup file {to set up the script in the task schduler and config registry keys for the user in github}
# the cursur shows the a circle spinning when teh script runs in the background
# https://learn.microsoft.com/fr-fr/windows/win32/apiindex/windows-api-list

import win32api as win
import time
import subprocess
import logging
import psutil
import winreg
from winotify import Notification, audio

# to avoid getting modulenotfounderror include all packges//modules here

# retreiving the battery life percent
battery_life_percent = win.GetSystemPowerStatus()['BatteryLifePercent']

isplugged_counter_value = 0x00000000  # false
# notification objects
battery_low_alert = Notification('SAVE UR BATTERY LIFE', 'LOW BATTERY',
                                 "2 MINS YOUR PC WILL SHUTDOWN\nPLEASE TURN IT OFF", 'D:/Desktop/cody/myworkenv/Battery-Low.ico', 'long')
plugged_and_on_alert = Notification('SAVE UR BATTERY LIFE', 'PLUGGED AND RUNNING',
                                    "PLEASE DO REMOVE THE PLUG WHILE USING THE LAPTOP", 'D:/Desktop/cody/myworkenv/Battery-Low.ico', 'long')
last_shutdown_alert = Notification('SAVE UR BATTERY LIFE', 'BYE,YOU MADE ME DO IT',
                                   "2 MINS LEFT YOUR PC WILL SHUTDOWN", 'D:/Desktop/cody/myworkenv/Battery-Low.ico', 'long')
# i used error handling to log any potential error
try:
    # registry keys path
    regedit_path = winreg.HKEY_CURRENT_USER
    # openning the sub-software key
    software = winreg.OpenKeyEx(regedit_path, r'SOFTWARE\\')
    # creating a new sub-key everytime
    new_key = winreg.CreateKey(software, 'SAVE_YOUR_BATTERY_SCRIPT')
    # logging file config
    logging.basicConfig(level=logging.WARNING, filename='D:/Desktop/cody/myworkenv/save_ur_battery.log',
                        filemode='a', format="%(asctime)s - %(levelname)s - %(message)s")

    if battery_life_percent <= 20:
        # playing sound for the toast
        battery_low_alert.set_audio(audio.Default, loop=False)
        # showing toast message
        battery_low_alert.show()
        # 2 mins before the shutdown
        time.sleep(120)  # 120 sec
        # logging info into the file
        logging.warning(
            'ACTION=SHUTDOWN::A WARNNING MSG HAS BEEN SENT DUE TO ::LOW BATTERY LIFE::')
        # shutting down the computer using bash command
        subprocess.run("shutdown /s")

    # if the power plugged in while using the computer do send a notification msg
    elif psutil.sensors_battery()[2] == True:
        # openning the last created sub-key from the registry
        key_folder = winreg.OpenKeyEx(
            regedit_path, r'SOFTWARE\\SAVE_YOUR_BATTERY_SCRIPT')
        # getting the current value stored in the registry
        isplugged_counter_value_reg = winreg.QueryValueEx(
            key_folder, 'isplugged_counter')
        # incrementing the value by 1 hexdecimal in the registry
        isplugged_counter_value = isplugged_counter_value_reg[0]+0x00000001
        # setting the value inside the registry to one
        winreg.SetValueEx(new_key, 'isplugged_counter', 3,
                          winreg.REG_DWORD, isplugged_counter_value)
        # if the user at the first popup didn't unplug the charger the second time pc will be shutdown
        if isplugged_counter_value == 2:
            # logging message into the file
            logging.warning(
                'ACTION=SHUTDOWN::A WARNNING MSG HAS BEEN SENT DUE TO ::PC IS ON AND CHARGING::')
            # playing sound for the toast
            last_shutdown_alert.set_audio(audio.Default, loop=False)
            # showing toast message
            last_shutdown_alert.show()
            # resetting the isplugged_counter_value to update the key to zero
            isplugged_counter_value = 0x00000000
            winreg.SetValueEx(new_key, 'isplugged_counter', 3,
                              winreg.REG_DWORD, isplugged_counter_value)

            # 2 mins before the shutdown
            time.sleep(120)
            # shutting down the computer using bash command
            subprocess.run("shutdown /s")
            # closing the key opened the hkey
            winreg.CloseKey(regedit_path)

        # if isplugged  counter is still 1 do this

        # playing sound for the toast
        plugged_and_on_alert.set_audio(audio.Default, loop=False)
        # showing toast message
        plugged_and_on_alert.show()

        logging.warning(
            'ACTION=NONE::A WARNNING MSG HAS BEEN SENT DUE TO ::PC IS ON AND CHARGING::')

# logging any potentiel errors inside the logging file
except Exception as e:
    logging.warning(e)
