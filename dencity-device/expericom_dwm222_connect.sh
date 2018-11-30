# This script connects a Raspberry Pi to Expericom with
# a DWM-222 USB modem.
#
# Tested with:
# Raspberry Pi 3 Model B+
# OS: Raspbian Stretch 2018-04-18
# Modem: D-link DWM-222
# Expericom SIM card
#
# How to:
# 1. Install wvdial on Raspberry Pi: "sudo apt-get install wvdial"
# 2. Transfer this script to the Raspberry Pi via, for example, scp.
# 3. Give it executable permission: chmod +x expericom_dwm222_connect.sh
# 4. Disconnect internet and restart the Raspberry Pi.
# 5. Run it: ./expericom_dwm222_connect.sh
# Note: The reason the apt-get of wvdial is not automated by the script is that
# the Raspberry Pi might have to be restarted after disconnecting to internet.
# Warning: It will overwrite the files, not append to them.

# Echo all commands
set -x

sudo sh -c "echo 'DisableSwitching=0\nDisableMBIMGlobal=0\nEnableLogging=0\nHuaweiAltModeGlobal=0\nDefaultVendor=0x2001\nDefaultProduct=0xab00\nTargetVendor=0x2001\TargetProduct=0x7e35\nStandardEject=1\n' > /etc/usb_modeswitch.conf"
sudo sh -c "echo '[Dialer Defaults]\nInit1 = ATZ\nInit2 = ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0\nInit3 = AT+CGDCONT=1,\"IP\",\"\"\nStupid Mode = 1\nModem Type = Analog Modem\nISDN = 0\nPhone = *99***1#\nModem = /dev/ttyUSB1\nUsername = { }\nPassword = { }\nBaud = 460800\n' > /etc/wvdial.conf"
sudo sh -c "echo 'noauth\nname wvdial\nusepeerdns\ndefaultroute\nreplacedefaultroute\n' > /etc/ppp/peers/wvdial"
sudo sh -c "echo 'nameserver 8.8.8.8' > /etc/resolv.conf"

sudo sh -c "usb_modeswitch -v 2001 -p ab00 -V 2001 -P 7e35 -K -W"
sudo sh -c "modprobe option"
sudo sh -c "echo 2001 7e35 > /sys/bus/usb-serial/drivers/option1/new_id"
sudo sh -c "wvdial"
