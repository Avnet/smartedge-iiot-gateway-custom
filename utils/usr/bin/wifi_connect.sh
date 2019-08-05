#/!bin/sh
zero=0
echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" >/etc/wpa_supplicant/wpa_supplicant.conf

echo "country=US" >>/etc/wpa_supplicant/wpa_supplicant.conf

echo "network={\r\n      key_mgmt=WPA-PSK\r\n" >>/etc/wpa_supplicant/wpa_supplicant.conf

echo "psk=" | tr -d "\r\n" >pskline
cat wifi_ssid_psk | cut -d ':' -f2  | tr -d "}" >>pskline
cat pskline >>/etc/wpa_supplicant/wpa_supplicant.conf
echo "ssid=" | tr -d "\r\n" >ssidline
cat wifi_ssid_psk | cut -d ':' -f1  | tr -d "{" >>ssidline
cat ssidline >>/etc/wpa_supplicant/wpa_supplicant.conf
echo "}\r\n" >>/etc/wpa_supplicant/wpa_supplicant.conf
#stop AP mode
sudo cp /etc/dhcpcd.conf.default /etc/dhcpcd.conf
sudo cp /etc/default/hostapd.default /etc/default/hostapd
sudo cp /etc/dnsmasq.conf.default /etc/dnsmasq.conf
sudo systemctl disable hostapd.service
sudo systemctl disable dnsmasq.service
sudo systemctl stop hostapd.service
sudo systemctl stop dnsmasq.service
# start client mode
sudo wpa_supplicant -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf &
sleep 10
sudo touch /tmp/ip_address
sudo chmod 777 /tmp/ip_address
sudo ifconfig wlan0 | grep inet >/tmp/ip_address
# check to see if we have an IP address specifically on wlan0
size=`stat -c%s /tmp/ip_address`

if [ $size != $zero ]
then
# have client IP
	sudo ./wifi_client.sh
else
#no client IP go back to AP mode
    pkill wpa_supplicant
    sudo cp /etc/dhcpcd.conf.ap /etc/dhcpcd.conf
    sudo cp /etc/default/hostapd.ap /etc/default/hostapd
    sudo cp /etc/dnsmasq.conf.ap /etc/dnsmasq.conf
    sudo systemctl enable hostapd.service
    sudo systemctl enable dnsmasq.service
    sudo systemctl start dnsmasq.service
    sudo systemctl start hostapd.service
fi
