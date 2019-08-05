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
#sudo ./rest.sh &
sudo /usr/bin/reboot.sh
