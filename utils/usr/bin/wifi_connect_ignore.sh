#/!bin/sh
zero=0
sleep 5 
sudo systemctl disable hostapd.service
sudo systemctl disable dnsmasq.service

sudo systemctl stop hostapd.service
sudo systemctl stop dnsmasq.service

# start client mode
sudo echo "SKIP" >/tmp/ip_address
sudo ./wifi_client.sh
