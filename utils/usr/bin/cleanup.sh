#!/bin/sh
sudo rm /usr/bin/IoTConnectSDK_Py2.7_Testing/sample/install*
sudo rm -R /usr/bin/IoTConnectSDK_Py2.7_Testing/sample/updates
sudo rm -R /home/avnet/*
sudo rm /home/avnet/.bash_history
sudo rm /root/.bash_history
sudo rm -R /var/log/*
sudo rm /etc/ssh/ssh_host_*
sudo rm /etc/*.txt
sudo rm /usr/bin/provisioning.txt
sudo rm /usr/bin/tmp?.txt
sudo rm /usr/bin/deviceid.txt
sudo rm /usr/bin/essidnames
sudo rm /usr/bin/signalvalues
sudo rm /usr/bin/essidlist
sudo rm /usr/bin/ssidline
sudo rm /usr/bin/pskline
sudo rm /usr/bin/wifi_ssid_psk
sudo rm /usr/bin/signallist
sudo rm /usr/bin/iwlist
sudo rm /etc/machine-id
sudo touch /etc/machine-id
#sudo dpkg-reconfigure openssh-server
sudo systemctl enable regenerate_ssh_host_keys
sudo rm /usr/bin/ImageDate.txt
sudo date >/usr/bin/ImageDate.txt
#Enable AP mode
sudo rm /etc/wpa_supplicant/wpa_supplicant.conf
sudo pkill wpa_supplicant
sudo pkill startup
sudo pkill rest
sudo pkill python
sudo rm /tmp/ip_address
sudo rm /tmp/iotconnect.txt
sudo cp /etc/rc.local.boot /etc/rc.local
sudo cp /etc/default/hostapd.ap /etc/default/hostapd
sudo cp /etc/dhcpcd.conf.ap /etc/dhcpcd.conf
sudo cp /etc/dnsmasq.conf.ap /etc/dnsmasq.conf
sudo systemctl daemon-reload
sudo systemctl enable dnsmasq.service
sudo systemctl enable hostapd.service
sudo systemctl start dnsmasq.service
sudo systemctl start hostapd.service
history -c
# NOTE: Either need to reboot or manually start the ap_mode services
sudo halt


