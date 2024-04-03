import urequests
import config
import machine
import asyncio
import os

# Over-The-Air (OTA) updates with MicroPython on supported devices.
# OTA updates allow you to remotely update the firmware or software on a device without needing physical access to it.
# This is particularly useful for IoT devices deployed in the field or in hard-to-reach places.
# The general process involves hosting the new firmware or script files on a server, and then having the device download and apply these updates over a network connection, typically Wi-Fi.

async def check_for_firmware_update():
    print('Checking for new firmware update @', config.VERSION_URL)
    try:
        response = urequests.get(config.VERSION_URL)
        if response.status_code == 200:
            server_version = float(response.text)
            device_version = float(config.device_version)
            print(f"Local ira version: {device_version} <= Server ira version: {server_version}")
            if server_version > device_version:
                print('Update available!')
                return True                
            else:
                print('No update needed.')
                return False
        else:
            print('Failed to fetch update information.')
            return False
    except Exception as e:
        print('Error checking for update:', str(e))
        return False
    
# We gaan op alle files controleren?
# Gaan we afdwingen om alles te wijzigen? (Force update vs only changed files)
async def update_firmware():
    #We need to get the version number and do update from that number.
    print('Firmware downloaded, reboot device in 3 seconds ...')
    await asyncio.sleep(3)
    # Reboot the device
    machine.reset()
    
async def flash_firmware(data):
    if len(data) != 2:
        print('No command arguments')
        return
    
    print('Start downloading specific firmware version:',data[1])
    create_directory(data[1])
    
    print('Firmware downloaded, reboot device in 3 seconds ...')
    #await asyncio.sleep(3)
    # Reboot the device
    #machine.reset()
    
# each version is placed in 1 directory.    
def create_directory(directory):
    try:
        os.mkdir(directory)
        print("Directory created:", directory)
    except OSError as e:
        # Check if the error is because the directory exists
        if 'EEXIST' in str(e):
            print("Directory already exists:", directory)
        else:
            # If the directory could not be created for a reason other than it already existing
            print("Error creating directory:", e)

# if we can create new versions we need to delete old one's 2. :-)
def delete_directory(directory):
    try:
        # List all directory contents
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                # If the item is a file, delete it
                os.remove(item_path)
            elif os.path.isdir(item_path):
                # If the item is a directory, recurse into it
                delete_directory(item_path)
        # After clearing all contents, delete the directory itself
        os.rmdir(directory)
        print("Deleted directory:", directory)
    except OSError as e:
        print("Error deleting directory:", e)